// mylib.c

#include "Python.h"
#include <stdio.h>


static PyObject *ErrorObject;
 

// 실제 동작하는 함수

static PyObject* write_log(PyObject *self, PyObject *args) // 인자는 이와같이 고정된다.
{
    char* msg;
    FILE *fp;
    
    if(!PyArg_ParseTuple(args, "s", &msg))
        return NULL;
    
    fp = fopen("c:\\pylog.txt", "wt+");
    fprintf(fp, msg);

    fclose(fp);
    
    return Py_BuildValue("i", 0);    
}
 

/* methods 구조체 배열에 지정되는 정보는 {"실제사용할 메쏘드명", 메쏘드명에 대응하는 실제 동작하는 함수명, 인자 종류} */

static struct PyMethodDef methods[] =
{
    {"wlog", write_log, METH_VARARGS},
    {NULL, NULL}
};

 

//

void initmylib()
{
    PyObject* m;
   

   // Py_InitModule("모듈명", 이모듈에 적용된 메쏘드들을 담을 구조체배열 포인터)
    m = Py_InitModule("mylib", methods);


    ErrorObject = Py_BuildValue("s", "error");
}
