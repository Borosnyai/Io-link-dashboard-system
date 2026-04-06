import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { HttpService } from '@nestjs/axios';
import { firstValueFrom } from 'rxjs';

@Injectable()
export class MasterService {
    constructor(private readonly configService: ConfigService,
        private readonly htppService: HttpService) { }

    getMasterConfig() {
        const baseUrl = this.configService.get<string>('MASTER_BASE_URL');
        const apiPath = this.configService.get<string>('MASTER_API_PATH');

        // Die zwei für die Echte Master gedacht! Das passiert bei Martin!
        //console.log('MASTER_BASE_URL =', baseUrl);
        //console.log('MASTER_API_PATH =', apiPath);

        return {
            baseUrl,
            apiPath,
            fullUrl: `${baseUrl}${apiPath}`,
        };
    }
    async testConnection() {
        const baseUrl = this.configService.get<string>('MASTER_BASE_URL');

        return {
            success: true,
            mode: 'mock',
            url: baseUrl,
            message: 'Mock connection to IO-Link Master is working',
        }
    }
}