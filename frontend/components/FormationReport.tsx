"use client";

import {
  FileText,
  Trophy,
  Layers3,
  BrainCircuit,
  Download,
} from "lucide-react";


export default function FormationReport({
  report,
  onDownloadPDF,
}: {
  report: any;
  onDownloadPDF: () => void;
}) {

  if (!report) {
    return null;
  }


  const best =
    report.best_reservoir;


  return (
  <div className="
    mt-8
    overflow-hidden
    rounded-2xl
    border
    border-white/10
    bg-white/[0.03]
  ">

    {/* REPORT HEADER */}

    <div className="
      flex
      items-center
      justify-between
      gap-4
      border-b
      border-white/10
      p-6
    ">

      {/* TITLE */}

      <div className="
        flex
        items-center
        gap-3
      ">

        <div className="
          flex
          h-10
          w-10
          items-center
          justify-center
          rounded-xl
          bg-white/10
        ">

          <FileText size={20} />

        </div>

        <div>

          <p className="
            text-base
            font-semibold
          ">
            {report.report_title}
          </p>

          <p className="
            mt-1
            text-xs
            text-gray-500
          ">
            Well: {report.well_id}
          </p>

        </div>

      </div>


      {/* DOWNLOAD BUTTON */}

      <button
        type="button"
        onClick={onDownloadPDF}
        className="
          flex
          items-center
          gap-2
          rounded-lg
          border
          border-white/10
          bg-white/10
          px-4
          py-2
          text-sm
          font-medium
          transition
          hover:bg-white/20
        "
      >

        <Download size={16} />

        Download PDF

      </button>

    </div>

      {best && (

        <div className="
          border-b
          border-white/10
          p-6
        ">

          <div className="
            flex
            items-center
            gap-2
            text-sm
            font-medium
          ">

            <Trophy size={17} />

            Best Candidate Reservoir

          </div>


          <div className="
            mt-4
            grid
            grid-cols-2
            gap-4
            md:grid-cols-4
          ">

            <div>

              <p className="
                text-xs
                text-gray-500
              ">
                Interval
              </p>

              <p className="mt-1 text-sm">
                {best.top}–{best.base} ft
              </p>

            </div>


            <div>

              <p className="
                text-xs
                text-gray-500
              ">
                Thickness
              </p>

              <p className="mt-1 text-sm">
                {best.gross_thickness} ft
              </p>

            </div>


            <div>

              <p className="
                text-xs
                text-gray-500
              ">
                Quality Score
              </p>

              <p className="
                mt-1
                text-lg
                font-semibold
              ">
                {best.quality_score}/100
              </p>

            </div>


            <div>

              <p className="
                text-xs
                text-gray-500
              ">
                Rank
              </p>

              <p className="mt-1 text-sm">
                #{best.quality_rank}
              </p>

            </div>

          </div>

        </div>

      )}


      {/* ZONE SUMMARY */}

      <div className="
        border-b
        border-white/10
        p-6
      ">

        <div className="
          flex
          items-center
          gap-2
          text-sm
          font-medium
        ">

          <Layers3 size={17} />

          Reservoir Zones

        </div>


        <div className="
          mt-4
          space-y-3
        ">

          {report.zones.map(
            (zone: any) => (

              <div
                key={zone.zone}
                className="
                  flex
                  items-center
                  justify-between
                  rounded-xl
                  border
                  border-white/10
                  bg-black/20
                  px-4
                  py-3
                "
              >

                <div>

                  <p className="text-sm">
                    Zone {zone.zone}
                  </p>

                  <p className="
                    mt-1
                    text-xs
                    text-gray-500
                  ">
                    {zone.top}–{zone.base} ft
                    {" · "}
                    {zone.thickness} ft
                  </p>

                </div>


                <p className="text-xs">
                  {zone.classification ===
                  "candidate_reservoir"
                    ? "Candidate Reservoir"
                    : "Non-reservoir"}
                </p>

              </div>

            )
          )}

        </div>

      </div>


      {/* AI INTERPRETATION */}

      <div className="
        flex
        items-center
        justify-between
        gap-4
        border-b
        border-white/10
        p-6
      ">

        <div className="
          flex
          items-center
          gap-2
          text-sm
          font-medium
        ">

          <BrainCircuit size={17} />

          AI Formation Evaluation

        </div>


        <div className="
          mt-4
          whitespace-pre-wrap
          text-sm
          leading-7
          text-gray-300
        ">

          {report.zone_interpretation}

        </div>

      </div>


      {/* DISCLAIMER */}

      <div className="
        p-6
      ">

        <p className="
          text-xs
          leading-5
          text-gray-500
        ">

          {report.disclaimer}

        </p>

      </div>

    </div>
  );
}