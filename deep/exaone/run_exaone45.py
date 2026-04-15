"""
EXAONE 4.5 기본 실행 샘플
- 모델: LGAI-EXAONE/EXAONE-4.5-7.8B-Instruct (또는 2.4B, 33B)
- 요구사항: pip install transformers torch accelerate
"""

import torch
from transformers import AutoProcessor
from transformers.models.exaone4_5.modeling_exaone4_5 import Exaone4_5_ForConditionalGeneration

# ── 모델 선택 ────────────────────────────────────────────────────────────────
# 사용 가능한 모델:
#   "LGAI-EXAONE/EXAONE-4.5-33B"       # 기본 (bfloat16, ~70GB VRAM)
#   "LGAI-EXAONE/EXAONE-4.5-33B-FP8"   # FP8 양자화 (~35GB VRAM)
MODEL_ID = "LGAI-EXAONE/EXAONE-4.5-33B"

# ── 프로세서 로드 (토크나이저 + 이미지 전처리 포함) ──────────────────────────
print(f"[1/3] 프로세서 로드: {MODEL_ID}")
processor = AutoProcessor.from_pretrained(
    MODEL_ID,
    trust_remote_code=True,
)
tokenizer = processor.tokenizer

# ── 모델 로드 ────────────────────────────────────────────────────────────────
print("[2/3] 모델 로드 중... (최초 실행 시 다운로드 시간이 걸립니다)")
model = Exaone4_5_ForConditionalGeneration.from_pretrained(
    MODEL_ID,
    dtype=torch.bfloat16,          # bfloat16으로 메모리 절약
    device_map="auto",             # GPU가 여러 개일 때 자동 분배
    trust_remote_code=True,
)
model.eval()
print(f"    device: {model.device}")

# ── transformers 버그 패치 ───────────────────────────────────────────────────
# ForConditionalGeneration.forward()가 model.embed_tokens / model.rotary_emb를 직접
# 참조하지만 실제 구조는 model.language_model.{embed_tokens,rotary_emb}에 있음
lm = model.model.language_model
if not hasattr(model.model, "embed_tokens"):
    model.model.embed_tokens = lm.embed_tokens
if not hasattr(model.model, "rotary_emb"):
    model.model.rotary_emb = lm.rotary_emb
print("    [패치] embed_tokens / rotary_emb 연결 완료")

# MTP(Multi-Token Prediction) 레이어 비활성화
# transformers 5.3.0.dev0에서 MTP attention mask shape 버그가 있어 우회
model.config.num_nextn_predict_layers = 0
print("    [패치] MTP 레이어 비활성화 완료")

# ── 추론 함수 ────────────────────────────────────────────────────────────────
def _normalize_messages(messages: list[dict]) -> list[dict]:
    """content가 list이면 text만 추출하여 문자열로 정규화합니다."""
    result = []
    for msg in messages:
        content = msg["content"]
        if isinstance(content, list):
            content = "".join(c.get("text", "") for c in content if c.get("type") == "text")
        result.append({"role": msg["role"], "content": content})
    return result


def chat(messages: list[dict], max_new_tokens: int = 512) -> str:
    """Chat 형식으로 모델에 질의하고 응답 텍스트를 반환합니다."""
    text = tokenizer.apply_chat_template(
        _normalize_messages(messages),
        tokenize=False,
        add_generation_prompt=True,
    )
    inputs = tokenizer(text, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.95,
            eos_token_id=tokenizer.eos_token_id,
            pad_token_id=tokenizer.eos_token_id,
        )

    # 입력 프롬프트 부분을 제외하고 생성된 토큰만 디코딩
    prompt_len = inputs["input_ids"].shape[1]
    return tokenizer.decode(outputs[0][prompt_len:], skip_special_tokens=True)


# ── 실행 예시 ────────────────────────────────────────────────────────────────
print("[3/3] 추론 시작\n" + "=" * 60)

# 예시 1: 단일 질문
messages = [
    {"role": "system", "content": [{"type": "text", "text": "You are EXAONE model from LG AI Research, a helpful assistant."}]},
    {"role": "user",   "content": [{"type": "text", "text": "EXAONE 4.5 모델의 주요 특징을 3가지 요약해줘."}]},
]

response = chat(messages, max_new_tokens=512)
print("[ 질문 ]", messages[-1]["content"])
print("[ 응답 ]")
print(response)
print("=" * 60)

# 예시 2: 멀티턴 대화
print("\n[ 멀티턴 대화 예시 ]")
history = [
    {"role": "system", "content": [{"type": "text", "text": "You are EXAONE model from LG AI Research, a helpful assistant."}]},
    {"role": "user",   "content": [{"type": "text", "text": "파이썬에서 리스트와 튜플의 차이를 설명해줘."}]},
]
answer1 = chat(history)
print("Q:", history[-1]["content"][0]["text"])
print("A:", answer1)

# 이전 응답을 히스토리에 추가하여 맥락 유지
history.append({"role": "assistant", "content": answer1})
history.append({"role": "user", "content": [{"type": "text", "text": "그럼 언제 튜플을 써야 해?"}]})
answer2 = chat(history)
print("\nQ:", history[-1]["content"][0]["text"])
print("A:", answer2)
