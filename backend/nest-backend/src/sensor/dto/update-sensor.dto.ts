import { IsInt, Max, Min } from 'class-validator';

export class UpdateSensorDto {
  @IsInt()
  @Min(0)
  @Max(1)
  value: number;
}

