import { Controller, Get } from '@nestjs/common';
import { SensorService } from './sensor.service';

@Controller('sensor')
export class SensorController {
  constructor(private readonly sensorService: SensorService) {}

  @Get('latest')
  getLatest() {
    return this.sensorService.getLatestMqttData();
  }
}