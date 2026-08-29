const API_URL = "http://localhost:8000";


export async function uploadDocument(
  file: File
) {

  const formData = new FormData();

  formData.append("file", file);


  const response = await fetch(
    `${API_URL}/documents/upload`,
    {
      method: "POST",
      body: formData,
    }
  );


  if (!response.ok) {

    const error = await response.json();

    throw new Error(
      error.detail || "Upload failed"
    );

  }


  return response.json();
}
export async function chatWithDocument(
  question: string,
  documentId?: string
) {
  const response = await fetch(
    `${API_URL}/chat`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question,
        document_id: documentId,
      }),
    }
  );

  if (!response.ok) {
    const error = await response.json();

    throw new Error(
      error.detail || "Chat request failed"
    );
  }

  return response.json();
}
export async function analyzeWell(
  wellId: string,
  settings: any
) {
  const response = await fetch(
    `${API_URL}/petrophysics/analyze/${wellId}`,
    {
      method: "POST",

      headers: {
        "Content-Type": "application/json",
      },

      body: JSON.stringify(settings),
    }
  );

  if (!response.ok) {

    const error =
      await response.json();

    throw new Error(
      error.detail ||
      "Well analysis failed"
    );
  }

  return response.json();
}