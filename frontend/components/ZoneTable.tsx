"use client";

import { Layers3 } from "lucide-react";

interface ZoneTableProps {
  zones: any[];
}

export default function ZoneTable({
  zones,
}: ZoneTableProps) {

  if (!zones.length) {
    return null;
  }

  return (
    <div className="
      mt-6
      overflow-hidden
      rounded-2xl
      border
      border-white/10
      bg-white/5
    ">

      <div className="
        border-b
        border-white/10
        px-5
        py-4
      ">

        <div className="
          flex
          items-center
          gap-3
        ">

          <Layers3 size={18} />

          <div>

            <p className="text-sm font-medium">
              Reservoir Zonation
            </p>

            <p className="text-xs text-gray-500">
              Automated interval classification
            </p>

          </div>

        </div>

      </div>


      <div className="overflow-x-auto">

        <table className="w-full text-sm">

          <thead>

            <tr className="
              border-b
              border-white/10
              text-xs
              text-gray-500
            ">

              <th className="px-5 py-3 text-left">
                Zone
              </th>

              <th className="px-5 py-3 text-left">
                Top
              </th>

              <th className="px-5 py-3 text-left">
                Base
              </th>

              <th className="px-5 py-3 text-left">
                Thickness
              </th>

              <th className="px-5 py-3 text-left">
                Classification
              </th>

              <th className="px-5 py-3 text-left">
                Vsh
              </th>

              <th className="px-5 py-3 text-left">
                Phi
              </th>

              <th className="px-5 py-3 text-left">
                Sw
              </th>

            </tr>

          </thead>


          <tbody>

            {zones.map(
              (zone) => (

                <tr
                  key={zone.zone}
                  className="
                    border-b
                    border-white/5
                    last:border-0
                  "
                >

                  <td className="px-5 py-4">
                    Zone {zone.zone}
                  </td>

                  <td className="px-5 py-4">
                    {zone.top} ft
                  </td>

                  <td className="px-5 py-4">
                    {zone.base} ft
                  </td>

                  <td className="
                    px-5
                    py-4
                    font-medium
                  ">
                    {zone.thickness} ft
                  </td>

                  <td className="px-5 py-4">

                    {zone.classification ===
                    "candidate_reservoir"
                      ? "Candidate Reservoir"
                      : "Non-reservoir"}

                  </td>

                  <td className="px-5 py-4">
                    {(zone.average_vsh * 100).toFixed(1)}%
                  </td>

                  <td className="px-5 py-4">
                    {(zone.average_porosity * 100).toFixed(1)}%
                  </td>

                  <td className="px-5 py-4">
                    {(zone.average_sw * 100).toFixed(1)}%
                  </td>

                </tr>

              )
            )}

          </tbody>

        </table>

      </div>

    </div>
  );
}