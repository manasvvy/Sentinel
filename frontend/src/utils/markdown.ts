export const parseMarkdown = (text: string): string => {
  // Basic markdown parsing for bold, italic, and code
  let result = text;

  // Bold
  result = result.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

  // Italic
  result = result.replace(/\*(.*?)\*/g, "<em>$1</em>");

  // Code blocks
  result = result.replace(
    /```([\s\S]*?)```/g,
    '<pre><code>$1</code></pre>'
  );

  // Inline code
  result = result.replace(/`(.*?)`/g, "<code>$1</code>");

  // Line breaks
  result = result.replace(/\n/g, "<br />");

  return result;
};

export const sanitizeHTML = (html: string): string => {
  // Basic sanitization - only allow specific tags
  const div = document.createElement("div");
  div.innerHTML = html;
  return div.textContent || div.innerText || "";
};
