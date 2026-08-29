"use client";

import {
  Sparkles,
  AlertTriangle,
} from "lucide-react";


interface FormationInterpretationProps {
  summary: any;
  interpretation: string;
}


export default function FormationInterpretation({
  summary,
  interpretation,
}: FormationInterpretationProps) {

  if (!summary) return null;


  return (
    <div className="
      mt-6
      rounded-2xl
      border
      border-white/10
      bg-white/5
      overflow-hidden
    ">

      {/* Header */}

      <div className="
        flex
        items-center
        gap-3
        border-b
        border-white/10
        px-5
        py-4
      ">

        <div className="
          flex
          h-9
          w-9
          items-center
          justify-center
          rounded-lg
          bg-white/10
        ">
          <Sparkles size={17} />
        </div>

        <div>

          <p className="text-sm font-medium">
            GeoMind Interpretation
          </p>

          <p className="text-xs text-gray-500">
            AI-assisted formation evaluation
          </p>

        </div>

      </div>


      {/* Summary */}

      <div className="
        grid
        grid-cols-2
        md:grid-cols-4
        gap-3
        p-5
      ">

        <Metric
          label="Avg. Vsh"
          value={`${(
            summary.average_vsh * 100
          ).toFixed(1)}%`}
        />

        <Metric
          label="Avg. Porosity"
          value={`${(
            summary.average_porosity * 100
          ).toFixed(1)}%`}
        />

        <Metric
          label="Avg. Sw"
          value={`${(
            summary.average_sw * 100
          ).toFixed(1)}%`}
        />

        <Metric
          label="Pay Thickness"
          value={`${(
            summary.pay_thickness
          ).toFixed(1)} m`}
        />

      </div>


      {/* Interpretation */}

      <div className="
        border-t
        border-white/10
        p-5
      ">

        <p className="
          mb-3
          text-xs
          uppercase
          tracking-wider
          text-gray-500
        ">
          Interpretation
        </p>

        <div className="
          whitespace-pre-wrap
          text-sm
          leading-7
          text-gray-300
        ">
          {interpretation}
        </div>

      </div>


      {/* Disclaimer */}

      <div className="
        flex
        gap-3
        border-t
        border-white/10
        bg-black/20
        px-5
        py-4
      ">

        <AlertTriangle
          size={15}
          className="mt-0.5 shrink-0"
        />

        <p className="text-xs leading-5 text-gray-500">
          AI interpretation is based on the
          selected petrophysical assumptions
          and should be reviewed by a qualified
          petrophysicist or subsurface professional.
        </p>

      </div>

    </div>
  );
}


function Metric({
  label,
  value,
}: {
  label: string;
  value: string;
}) {

  return (
    <div className="
      rounded-xl
      border
      border-white/10
      bg-black/20
      p-4
    ">

      <p className="text-xs text-gray-500">
        {label}
      </p>

      <p className="
        mt-2
        text-lg
        font-semibold
      ">
        {value}
      </p>

    </div>
  );
}