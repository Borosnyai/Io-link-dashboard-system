export interface Mapping {
  val: number | boolean;
  text: string;
}

export interface SensorValue {
  subindex: number;
  name: string;
  mappings: Mapping[];
}

export interface Sensor {
  name: string;
  index: number;
  values: SensorValue[];
}
