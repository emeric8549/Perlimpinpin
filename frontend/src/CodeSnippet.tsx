import React from "react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";

type CodeSnippetProps = {
  code: string;
  language: string;
};

const CodeSnippet: React.FC<CodeSnippetProps> = ({ code, language }) => {
  return (
    <div className="rounded-xl shadow-md p-4 bg-gray-900">
      <SyntaxHighlighter language={language} style={oneDark} showLineNumbers>
        {code}
      </SyntaxHighlighter>
    </div>
  );
};

export default CodeSnippet;