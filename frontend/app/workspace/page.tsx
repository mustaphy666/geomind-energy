"use client";

import { useRef, useState } from "react";

import {
  FileText,
  Upload,
  Send,
  Plus,
  Sparkles,
  Download
} from "lucide-react";
import WellLogViewer from "@/components/WellLogViewer";
import WellUpload from "@/components/WellUpload";
import {
  uploadDocument,
  chatWithDocument,
  analyzeWell,      
} from "@/lib/api";
import PetrophysicsSettings from "@/components/PetrophysicsSettings";
import FormationInterpretation from "@/components/FormationInterpretation";
import PayIntervalTable from "@/components/PayIntervalTable";
import ReservoirIntervalTable
  from "@/components/ReservoirIntervalTable";
import ZoneTable from "@/components/ZoneTable";
import ReservoirQuality from "@/components/ReservoirQuality";
import DataQualityCard
  from "@/components/DataQualityCard";

import FormationReport
  from "@/components/FormationReport";
export default function Workspace() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState<any[]>([]);
  const [asking, setAsking] = useState(false);
  const [selectedDocument, setSelectedDocument] =
    useState<any | null>(null);
  const [zones, setZones] =
  useState<any[]>([]);
  const [documents, setDocuments] = useState<any[]>([]);
  const [uploading, setUploading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [wellData, setWellData] = useState<any[]>([]);

  const [analyzingWell, setAnalyzingWell] =
    useState(false);
  const [wellId, setWellId] = useState<string | null>(
   null
   );
  const [wellInfo, setWellInfo] = useState<any | null>(
  null
);
  const [reservoirQuality, setReservoirQuality] =
  useState<any[]>([]);
  const [dataQuality, setDataQuality] =
  useState<any | null>(null);
  const [report, setReport] =
  useState<any | null>(null);
  const [reservoirIntervals, setReservoirIntervals] =
  useState<any[]>([]);
  const [formationSummary, setFormationSummary] =
  useState<any | null>(null);
  const [payIntervals, setPayIntervals] =
  useState<any[]>([]);
  const [aiInterpretation, setAiInterpretation] =
  useState("");
  
  const [petroSettings, setPetroSettings] =
  useState({
    gr_clean: 20,
    gr_shale: 120,

    rho_matrix: 2.65,
    rho_fluid: 1.0,

    rw: 0.05,

    a: 1.0,
    m: 2.0,
    n: 2.0,

    vsh_cutoff: 0.40,
    porosity_cutoff: 0.10,
    sw_cutoff: 0.60,
  });
async function handleUpload(
  event: React.ChangeEvent<HTMLInputElement>
) {

  const file = event.target.files?.[0];

  if (!file) return;


  if (file.type !== "application/pdf") {

    alert("Please upload a PDF file.");

    return;
  }


  try {

    setUploading(true);


    const result = await uploadDocument(file);


    setDocuments((previous) => [
      ...previous,
      result,
    ]);


  } catch (error) {

    console.error(error);

    alert("Something went wrong while uploading.");


  } finally {

    setUploading(false);

  }
}
async function handleAsk() {
  if (!question.trim()) return;

  if (!selectedDocument) {
    alert("Please upload and select a document first.");
    return;
  }

  try {
    setAsking(true);
    setAnswer("");
    setSources([]);

    const result = await chatWithDocument(
      question,
      selectedDocument.document_id
    );

    setAnswer(result.answer);
    setSources(result.sources || []);

  } catch (error) {
    console.error(error);

    setAnswer(
      "Sorry, I couldn't process that question."
    );

  } finally {
    setAsking(false);
  }
}
async function handleWellAnalysis() {

  if (!wellId) return;

  try {

    setAnalyzingWell(true);

    const result =
      await analyzeWell(
        wellId,
        petroSettings
      );

    console.log(
      "Petrophysical analysis:",
      result
    );

    
    setFormationSummary(
  result.summary
);
        setZones(
  result.zones || []
);
    

    setReservoirIntervals(
  Array.isArray(result.reservoir_intervals) 
    ? result.reservoir_intervals 
    : result.reservoir_intervals?.reservoir || []
); 
    setReservoirQuality(
  result.reservoir_quality || []
);
    setDataQuality(
    result.data_quality || null
);
    setReport(
  result.report || null
);
    setPayIntervals(
  Array.isArray(result.pay_intervals) 
    ? result.pay_intervals 
    : result.pay_intervals?.pay || []
);
    setAiInterpretation(
  result.interpretation
);
    setWellData(
      result.data
    );

  } catch (error) {

    console.error(error);

    alert(
      error instanceof Error
        ? error.message
        : "Well analysis failed"
    );

  } finally {

    setAnalyzingWell(false);

  }
}
const handleDownloadPDF = async () => {

  if (!report) {
    return;
  }

  try {

    const response = await fetch(
      "http://127.0.0.1:8000/petrophysics/report/pdf",
      {
        method: "POST",

        headers: {
          "Content-Type":
            "application/json",
        },

        body: JSON.stringify(report),
      }
    );

    if (!response.ok) {
      throw new Error(
        "Failed to generate PDF"
      );
    }

    const blob =
      await response.blob();

    const url =
      window.URL.createObjectURL(
        blob
      );

    const link =
      document.createElement("a");

    link.href = url;

    link.download =
      "GeoMind_Formation_Report.pdf";

    document.body.appendChild(link);

    link.click();

    link.remove();

    window.URL.revokeObjectURL(url);

  } catch (error) {

    console.error(
      "PDF generation failed:",
      error
    );

  }
};

  return (
    <main className="min-h-screen bg-black text-white flex">

      {/* Sidebar */}
      <aside className="w-72 border-r border-white/10 p-5 flex flex-col">

        {/* Logo */}
        <div className="flex items-center gap-3 mb-10">
          <div className="h-9 w-9 rounded-xl bg-white text-black flex items-center justify-center">
            <Sparkles size={18} />
          </div>

          <div>
            <h1 className="font-semibold">
              GeoMind
            </h1>

            <p className="text-xs text-gray-500">
              AI for Geoscience
            </p>
          </div>
        </div>


        {/* Upload */}
        
        <button
            onClick={() => fileInputRef.current?.click()}
            disabled={uploading}
            className="
                flex items-center justify-center gap-2
                rounded-xl
                bg-white
                text-black
                px-4
                py-3
                text-sm
                font-medium
                hover:bg-gray-200
                transition
                disabled:opacity-50
            "
            >
            <Upload size={17} />

            {uploading
                ? "Processing..."
                : "Upload Document"}
            </button>
            

            <input
            ref={fileInputRef}
            type="file"
            accept=".pdf"
            onChange={handleUpload}
            className="hidden"
            />



        {/* Documents */}
        <div className="mt-8">

          <p className="text-xs uppercase tracking-wider text-gray-500 mb-3">
            Documents
          </p>

         {documents.length === 0 ? (

  <div className="text-sm text-gray-600 text-center py-10">
    No documents yet
  </div>

) : (

  <div className="space-y-2">

    {documents.map((document) => (

      <div
        key={document.document_id}
        onClick={() => setSelectedDocument(document)}
        className={`
            flex
            items-center
            gap-3
            rounded-xl
            p-3
            cursor-pointer
            transition
            ${
            selectedDocument?.document_id === document.document_id
                ? "bg-white/10"
                : "hover:bg-white/5"
            }
        `}
        >

        <FileText
          size={18}
          className="text-gray-400"
        />

        <div className="min-w-0">

          <p className="text-sm truncate">
            {document.filename}
          </p>

          <p className="text-xs text-gray-600">
            {document.chunks} chunks
          </p>

        </div>

      </div>

    ))}

  </div>

)}

        </div>

      </aside>


      {/* Main workspace */}
      <section className="flex-1 flex flex-col">

        {/* Header */}
        <header className="h-16 border-b border-white/10 flex items-center px-8">

          <div>
            <h2 className="font-medium">
              Geological Intelligence
            </h2>

            <p className="text-xs text-gray-500">
              Analyze your geological data with AI
            </p>
          </div>

        </header>


        {/* Chat area */}
        <div className="flex-1 flex flex-col items-center justify-center px-6">

          <div className="max-w-2xl w-full text-center">

            <div className="mx-auto mb-6 h-16 w-16 rounded-2xl border border-white/10 flex items-center justify-center">

              <Sparkles size={28} />

            </div>


            <h2 className="text-3xl font-semibold mb-3">
              Welcome to GeoMind
            </h2>
            {answer && (
                <div className="mb-8 text-left">

                    <div className="rounded-2xl border border-white/10 bg-white/5 p-6">

                    <div className="flex items-center gap-2 mb-4">
                        <Sparkles size={17} />

                        <span className="text-sm font-medium">
                        GeoMind
                        </span>
                    </div>

                    <p className="text-gray-300 leading-7 whitespace-pre-wrap">
                        {answer}
                    </p>

                    </div>


                    {sources.length > 0 && (
                    <div className="mt-4">

                        <p className="text-xs uppercase tracking-wider text-gray-500 mb-2">
                        Sources
                        </p>

                        <div className="space-y-2">

                        {sources.map((source, index) => (
                            <div
                            key={index}
                            className="text-xs text-gray-500"
                            >
                            📄 {source.filename}
                            {" · "}
                            relevance: {source.score.toFixed(2)}
                            </div>
                        ))}

                        </div>

                    </div>
                    )}

                </div>
                )}


            <p className="text-gray-500 mb-10">
              Upload a geological document and ask questions
              about its contents.
            </p>


            {/* Input */}
            <div className="relative">

              <input
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                onKeyDown={(e) => {
                    if (e.key === "Enter") {
                    handleAsk();
                    }
                }}
                placeholder={
                    selectedDocument
                    ? `Ask about ${selectedDocument.filename}...`
                    : "Upload a document first..."
                }
                disabled={!selectedDocument || asking}
                className="
                  w-full
                  rounded-2xl
                  border
                  border-white/10
                  bg-white/5
                  px-5
                  py-4
                  pr-14
                  outline-none
                  focus:border-white/30
                  transition
                  disabled:opacity-50
                "
              />

              <button
                onClick={handleAsk}
                disabled={!question.trim() || !selectedDocument || asking}
                className="
                  absolute
                  right-2
                  top-2
                  h-10
                  w-10
                  rounded-xl
                  bg-white
                  text-black
                  flex
                  items-center
                  justify-center
                  hover:bg-gray-200
                  transition
                "
              >
                <Send size={17} />
              </button>
               
              <WellUpload
                onUploaded={(result) => {

                    console.log(
                    "Well uploaded:",
                    result
                    );

                    setWellId(
                    result.well_id
                    );
                    setWellInfo(result);

                }}
              />
              {wellInfo && (
  <div className="mt-4 rounded-xl border border-white/10 bg-white/5 p-4">

    <div className="flex items-center gap-3 mb-4">

      <FileText size={18} />

      <div>
        <p className="text-sm font-medium">
          {wellInfo.filename}
        </p>

        <p className="text-xs text-gray-500">
          Well uploaded successfully
        </p>
      </div>

    </div>


    <div className="grid grid-cols-2 gap-3 text-xs">

      <div>
        <p className="text-gray-500">
          Well
        </p>

        <p>
          {wellInfo.metadata?.well_name || "Unknown"}
        </p>
      </div>


      <div>
        <p className="text-gray-500">
          Curves
        </p>

        <p>
          {wellInfo.metadata?.curve_count || 0}
        </p>
      </div>


      <div>
        <p className="text-gray-500">
          Start Depth
        </p>

        <p>
          {wellInfo.metadata?.start_depth}
        </p>
      </div>


      <div>
        <p className="text-gray-500">
          End Depth
        </p>

        <p>
          {wellInfo.metadata?.end_depth}
        </p>
      </div>

    </div>


    <div className="mt-4">

      <p className="text-xs text-gray-500 mb-2">
        Available Curves
      </p>

      <div className="flex flex-wrap gap-2">

        {wellInfo.curves?.map(
                (curve: any) => (

                    <span
                    key={curve.mnemonic}
                    className="
                        rounded-lg
                        border
                        border-white/10
                        bg-white/5
                        px-2
                        py-1
                        text-xs
                    "
                    >
                    {curve.mnemonic}
                    </span>

                )
                )}

            </div>

            </div>

        </div>
        )}
              {wellData.length > 0 && (
                <div className="mt-8">

                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">

                    <div className="rounded-xl border border-white/10 bg-white/5 p-5">
                        <p className="text-xs text-gray-500">
                        Avg. Vshale
                        </p>

                        <p className="mt-2 text-2xl font-semibold">
                        {(
                            wellData.reduce(
                            (sum, row) =>
                                sum + (row.VSH || 0),
                            0
                            ) / wellData.length * 100
                        ).toFixed(1)}%
                        </p>
                    </div>


                    <div className="rounded-xl border border-white/10 bg-white/5 p-5">
                        <p className="text-xs text-gray-500">
                        Avg. Porosity
                        </p>

                        <p className="mt-2 text-2xl font-semibold">
                        {(
                            wellData.reduce(
                            (sum, row) =>
                                sum + (row.POROSITY || 0),
                            0
                            ) / wellData.length * 100
                        ).toFixed(1)}%
                        </p>
                    </div>


                    <div className="rounded-xl border border-white/10 bg-white/5 p-5">
                        <p className="text-xs text-gray-500">
                        Avg. Water Saturation
                        </p>

                        <p className="mt-2 text-2xl font-semibold">
                        {(
                            wellData.reduce(
                            (sum, row) =>
                                sum + (row.SW || 0),
                            0
                            ) / wellData.length * 100
                        ).toFixed(1)}%
                        </p>
                    </div>


                    <div className="rounded-xl border border-white/10 bg-white/5 p-5">
                        <p className="text-xs text-gray-500">
                        Pay Points
                        </p>

                        <p className="mt-2 text-2xl font-semibold">
                        {
                            wellData.filter(
                            (row) => row.PAY
                            ).length
                        }
                        </p>
                    </div>

                    </div>

                </div>
                )}
                {wellInfo && (
  <div className="mt-6">

    <PetrophysicsSettings
      settings={petroSettings}
      setSettings={setPetroSettings}
      onAnalyze={handleWellAnalysis}
      analyzing={analyzingWell}
    />

  </div>
)}
              {wellInfo && (
                <button
                    onClick={handleWellAnalysis}
                    disabled={analyzingWell}
                    className="
                    mt-4
                    w-full
                    rounded-xl
                    bg-white
                    px-4
                    py-3
                    text-sm
                    font-medium
                    text-black
                    transition
                    hover:bg-gray-200
                    disabled:opacity-50
                    "
                >
                    {analyzingWell
                    ? "Analyzing Well..."
                    : "Run Formation Evaluation"}
                </button>
                )}
                {dataQuality && (
  <DataQualityCard
    report={dataQuality}
  />
)}
                {zones.length > 0 && (
  <ZoneTable
    zones={zones}
  />
)}
                {reservoirIntervals.length > 0 && (
  <ReservoirIntervalTable
    intervals={Array.isArray(reservoirIntervals) ? reservoirIntervals : []}
  />
)}
                {reservoirQuality.length > 0 && (
  <ReservoirQuality
    intervals={reservoirQuality}
  />
)}
                {wellData.length > 0 && (
  <PayIntervalTable
    intervals={Array.isArray(payIntervals) ? payIntervals : []}
  />
)}
                 {formationSummary && (
  <FormationInterpretation
    summary={formationSummary}
    interpretation={aiInterpretation}
  />
)}
                {report && (
  <FormationReport
    report={report}
    onDownloadPDF={handleDownloadPDF}
  />
)}
                {wellData.length > 0 && (
                <div className="mt-8">
                    <WellLogViewer
                    data={wellData}
                    />
                </div>
                )}
                
              
            </div>

          </div>

        </div>

      </section>

    </main>
  );
}
