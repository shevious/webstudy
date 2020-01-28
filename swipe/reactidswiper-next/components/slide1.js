import { Flex } from "@react-yuki/ui";
import Text1 from "./text1";

const Slide1 = () => (
  <Flex
    maxHeight="20rem"
    alignItems="top"
    justifyContent="center"
    color="white"
    className="swiper-slide"
    bg="#44d9cd"
  >
    <Text1 />
  </Flex>
);

export default Slide1;

