"use client";

import { useRef, useState } from "react";
import { Upload, FileChartColumn } from "lucide-react";

const API_URL = "http://localhost:8000";

interface WellUploadProps {
  onUploaded: (
    result: any
  ) => void;
}

export default function WellUpload({
  onUploaded,
}: WellUploadProps) {

  const inputRef =
    useRef<HTMLInputElement>(null);

  const [uploading, setUploading] =
    useState(false);


  async function handleUpload(
    event: React.ChangeEvent<HTMLInputElement>
  ) {

    const file =
      event.target.files?.[0];

    if (!file) return;


    if (
      !file.name
        .toLowerCase()
        .endsWith(".las")
    ) {

      alert(
        "Please select a LAS file."
      );

      return;
    }


    const formData =
      new FormData();

    formData.append(
      "file",
      file
    );


    try {

      setUploading(true);

      const response =
        await fetch(
          `${API_URL}/welllogs/upload`,
          {
            method: "POST",
            body: formData,
          }
        );


      if (!response.ok) {

        const error =
          await response.json();

        throw new Error(
          error.detail ||
          "LAS upload failed"
        );
      }


      const result =
        await response.json();


      onUploaded(result);


    } catch (error) {

      console.error(error);

      alert(
        error instanceof Error
          ? error.message
          : "Upload failed"
      );

    } finally {

      setUploading(false);

    }
  }


  return (
    <div>

      <input
        ref={inputRef}
        type="file"
        accept=".las"
        onChange={handleUpload}
        className="hidden"
      />


      <button
        onClick={() =>
          inputRef.current?.click()
        }
        disabled={uploading}
        className="
          flex
          items-center
          gap-3
          w-full
          rounded-xl
          border
          border-white/10
          bg-white/5
          px-4
          py-4
          hover:bg-white/10
          transition
          disabled:opacity-50
        "
      >

        <div className="
          h-10
          w-10
          rounded-lg
          bg-white/10
          flex
          items-center
          justify-center
        ">
          <FileChartColumn size={19} />
        </div>


        <div className="text-left">

          <p className="text-sm font-medium">
            {uploading
              ? "Processing LAS..."
              : "Upload Well Log"}
          </p>

          <p className="text-xs text-gray-500">
            LAS 2.0 / well-log data
          </p>

        </div>

        <Upload
          size={17}
          className="ml-auto text-gray-500"
        />

      </button>

    </div>
  );
}
