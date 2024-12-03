export const uploadFiles = async (formData) => {
  const response = await fetch("http://127.0.0.1:5000/upload", {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to upload files.");
  }

  return response.json();
};
