import { Module } from '@nestjs/common';
import { SensorModule } from './sensor/sensor.module';

@Module({
  imports: [SensorModule],
})
export class AppModule {}