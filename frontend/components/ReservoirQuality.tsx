"use client";

import {
  Trophy,
} from "lucide-react";


interface ReservoirQualityProps {
  intervals: any[];
}


export default function ReservoirQuality({
  intervals,
}: ReservoirQualityProps) {

  if (!intervals.length) {
    return null;
  }


  return (
    <div className="
      mt-6
      rounded-2xl
      border
      border-white/10
      bg-white/5
      overflow-hidden
    ">

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

          <Trophy size={18} />

        </div>


        <div>

          <p className="text-sm font-medium">
            Reservoir Quality Ranking
          </p>

          <p className="
            text-xs
            text-gray-500
          ">
            Screening score based on
            calculated petrophysical properties
          </p>

        </div>

      </div>


      <div className="p-5 space-y-4">

        {intervals.map(
          (interval) => {

            const score =
              interval.quality_score;

            return (

              <div
                key={interval.quality_rank}
                className="
                  rounded-xl
                  border
                  border-white/10
                  bg-black/20
                  p-4
                "
              >

                <div className="
                  flex
                  items-center
                  justify-between
                  gap-4
                ">

                  <div>

                    <p className="
                      text-sm
                      font-medium
                    ">
                      #{interval.quality_rank}
                      {" "}
                      {interval.top}–
                      {interval.base} ft
                    </p>

                    <p className="
                      mt-1
                      text-xs
                      text-gray-500
                    ">
                      {interval.gross_thickness} ft
                      {" "}gross interval
                    </p>

                  </div>


                  <div className="
                    text-right
                  ">

                    <p className="
                      text-xl
                      font-semibold
                    ">
                      {score}
                    </p>

                    <p className="
                      text-[10px]
                      uppercase
                      tracking-wider
                      text-gray-500
                    ">
                      / 100
                    </p>

                  </div>

                </div>


                <div className="
                  mt-4
                  h-2
                  overflow-hidden
                  rounded-full
                  bg-white/10
                ">

                  <div
                    className="
                      h-full
                      rounded-full
                      bg-white
                    "
                    style={{
                      width: `${score}%`,
                    }}
                  />

                </div>


                <div className="
                  mt-3
                  grid
                  grid-cols-3
                  gap-3
                  text-xs
                ">

                  <div>
                    <span className="text-gray-500">
                      Vsh
                    </span>

                    <p className="mt-1">
                      {(
                        interval.average_vsh
                        * 100
                      ).toFixed(1)}%
                    </p>
                  </div>


                  <div>
                    <span className="text-gray-500">
                      Porosity
                    </span>

                    <p className="mt-1">
                      {(
                        interval.average_porosity
                        * 100
                      ).toFixed(1)}%
                    </p>
                  </div>


                  <div>
                    <span className="text-gray-500">
                      Sw
                    </span>

                    <p className="mt-1">
                      {(
                        interval.average_sw
                        * 100
                      ).toFixed(1)}%
                    </p>
                  </div>

                </div>

              </div>

            );
          }
        )}

      </div>


      <div className="
        border-t
        border-white/10
        px-5
        py-4
      ">

        <p className="
          text-xs
          leading-5
          text-gray-500
        ">

          RQS is a project-specific screening
          metric, not a standardized industry
          reservoir-quality index. It should
          not be used as a standalone basis
          for reserves or development decisions.

        </p>

      </div>

    </div>
  );
}