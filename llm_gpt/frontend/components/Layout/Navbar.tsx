import Link from "next/link";
import { FC } from "react";

export const Navbar: FC = () => {
  return (
    <div className="flex h-[50px] sm:h-[60px] border-b border-neutral-300 py-2 px-2 sm:px-8 items-center justify-between">
      {/* Left side: title */}
      <div className="font-bold text-3xl flex items-center">
        <Link href="/" className="ml-2 hover:opacity-50">
          CHATBOT LLM-GPT-Demo
        </Link>
      </div>

      {/* Right side: social links */}
      <div className="flex space-x-4 items-center">
        <Link
          href="https://www.linkedin.com/in/alexandre-sanou-bb3b74101/"
          target="_blank"
          rel="noopener noreferrer"
          className="hover:opacity-50"
        >
          {/* You can replace text with an icon component or SVG */}
          LinkedIn
        </Link>
        <Link
          href="https://github.com/SanouAlexandre"
          target="_blank"
          rel="noopener noreferrer"
          className="hover:opacity-50"
        >
          GitHub
        </Link>
      </div>
    </div>
  );
};
