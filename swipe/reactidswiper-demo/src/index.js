import React from "react";
import ReactDOM from "react-dom";
import { ThemeProvider, createGlobalStyle } from "styled-components";
import { Box, Heading, theme, normalize } from "@react-yuki/ui";
import generateData from "./data";
import Slider from "./slider";

import "react-id-swiper/lib/styles/scss/swiper.scss";
import "./styles.scss";

const Styles = createGlobalStyle`
  ${normalize}

  html,
  body {
    background-color: ${theme.colors.white};
    font-family: ${theme.fonts.base};
    color: ${theme.colors.dark};
    font-size: 16px;
    -moz-osx-font-smoothing: grayscale;
    -webkit-font-smoothing: antialiased;
    overflow-x: hidden;
    overflow-y: scroll;
    text-rendering: optimizeLegibility;
    text-size-adjust: 100%;
    padding: 0;
    margin: 0;
    width: 100%;
    height: 100%;

    * {
      box-sizing: border-box;
    }

    a, button {
      cursor: pointer;
    }

    a {
      text-decoration: none;

      &:hover {
        text-decoration: underline;
      }
    }

    button {
      &:focus {
        outline: 0;
      }
    }
  }
`;

const App = () => (
  <ThemeProvider theme={theme}>
    <>
      <Styles />
      <Box p={4}>
        <Box>
          <Heading
            as="h1"
            color="orange.4"
            fontSize={13}
            m={0}
            my={4}
            fontWeight={1}
            textAlign="center"
          >
            React Id Swiper DEMO
          </Heading>
          <Heading
            m={0}
            my={4}
            textAlign="center"
            color="blue.4"
            as="h3"
            fontWeight={2}
          >
            Please reproduce your issues here!!!!
          </Heading>
        </Box>
        <Box>
          <Slider items={generateData()} />
        </Box>
      </Box>
    </>
  </ThemeProvider>
);

const rootElement = document.getElementById("root");

ReactDOM.render(<App />, rootElement);
