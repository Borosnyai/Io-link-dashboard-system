import { Module } from '@nestjs/common';
import { MasterService } from './master.service';
import { MasterController } from './master.controller';
import { HttpModule } from '@nestjs/axios';

@Module({
  imports: [HttpModule],  
  providers: [MasterService],
  controllers: [MasterController],
  exports: [MasterService],
})
export class MasterModule {}
