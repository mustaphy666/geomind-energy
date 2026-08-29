"use client";

import {
  ShieldCheck,
  AlertTriangle,
} from "lucide-react";


export default function DataQualityCard({
  report,
}: {
  report: any;
}) {

  if (!report) {
    return null;
  }


  const good =
    report.status === "excellent" ||
    report.status === "good";


  return (
    <div className="
      mt-6
      rounded-2xl
      border
      border-white/10
      bg-white/5
      p-5
    ">

      <div className="
        flex
        items-center
        gap-3
      ">

        {good ? (
          <ShieldCheck size={20} />
        ) : (
          <AlertTriangle size={20} />
        )}

        <div>

          <p className="text-sm font-medium">
            Log Data Quality
          </p>

          <p className="
            text-xs
            text-gray-500
          ">
            Pre-analysis data assessment
          </p>

        </div>

      </div>


      <div className="
        mt-5
        flex
        items-end
        justify-between
      ">

        <div>

          <p className="
            text-3xl
            font-semibold
          ">
            {report.score}
          </p>

          <p className="
            text-xs
            text-gray-500
          ">
            / 100 completeness
          </p>

        </div>


        <p className="
          text-sm
          capitalize
        ">
          {report.status}
        </p>

      </div>


      <div className="
        mt-4
        h-2
        rounded-full
        bg-white/10
        overflow-hidden
      ">

        <div
          className="
            h-full
            rounded-full
            bg-white
          "
          style={{
            width: `${report.score}%`,
          }}
        />

      </div>


      <div className="
        mt-5
        grid
        grid-cols-2
        gap-3
      ">

        {Object.entries(
          report.curve_completeness
        ).map(
          ([curve, value]: any) => (

            <div
              key={curve}
              className="
                rounded-lg
                border
                border-white/10
                bg-black/20
                p-3
              "
            >

              <p className="
                text-xs
                text-gray-500
              ">
                {curve}
              </p>

              <p className="mt-1 text-sm">
                {value}%
              </p>

            </div>

          )
        )}

      </div>


      {report.missing_curves?.length > 0 && (

        <div className="
          mt-4
          text-xs
          text-gray-500
        ">

          Missing curves:{" "}
          {report.missing_curves.join(", ")}

        </div>

      )}

    </div>
  );
}