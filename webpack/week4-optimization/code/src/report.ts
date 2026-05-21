import dayjs from "dayjs";

export function createReportText(total: number, sample: number[]): string {
  return [
    `now: ${dayjs().format("YYYY-MM-DD HH:mm:ss")}`,
    `array-size: ${total}`,
    `sample: ${sample.join(", ")}`
  ].join("\n");
}
