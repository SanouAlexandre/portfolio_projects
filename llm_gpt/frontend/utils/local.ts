import { Message } from "@/types";
const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const LocalAIStream = async (messages: Message[]) => {
  const res = await fetch(`${apiUrl}`, {
    headers: {
      "Content-Type": "application/json",
    },
    method: "POST",
    body: JSON.stringify({
      user_input: messages[messages.length - 1].content,
    }),
  });

  if (res.status !== 200) {
    throw new Error("Local API returned an error");
  }

  const json = await res.json();
  console.log("bot_response: ", json.content);

  return json.content;
};
