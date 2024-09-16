export async function generateContent(formData) {
  // In a real implementation, you would send the formData to your AI service
  // and receive the generated content in return.
  // For this example, we'll simulate the process with a timeout.

  return new Promise((resolve) => {
    setTimeout(() => {
      const mockContent = {
        type: formData.outputType,
        url: 'https://example.com/generated-content.jpg',
      };
      resolve(mockContent);
    }, 2000);
  });
}