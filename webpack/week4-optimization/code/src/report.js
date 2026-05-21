import dayjs from "dayjs";

export function createReportText(total, sample) {
  return [
    `now: ${dayjs().format("YYYY-MM-DD HH:mm:ss")}`,
    `array-size: ${total}`,
    `sample: ${sample.join(", ")}`
  ].join("\n");
}
