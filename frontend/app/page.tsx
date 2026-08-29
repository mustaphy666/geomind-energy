 
"use client";

import { useEffect, useState } from "react";

export default function Home() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetch("http://127.0.0.1:8000/")
      .then((res) => res.json())
      .then((data) => setMessage(data.message))
      .catch(() => setMessage("Backend not connected"));
  }, []);

  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-black text-white">
      <h1 className="text-6xl font-bold mb-4">GeoMind AI</h1>

      <p className="text-gray-400 mb-8">
        The AI Operating System for Geoscience
      </p>

      <div className="rounded-xl border border-gray-700 px-6 py-4">
        {message}
      </div>
    </main>
  );
}