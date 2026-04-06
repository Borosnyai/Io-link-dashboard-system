import { Injectable, OnModuleInit, OnModuleDestroy } from '@nestjs/common';
import * as mqtt from 'mqtt';

@Injectable()
export class SensorService implements OnModuleInit, OnModuleDestroy {
  private client: mqtt.MqttClient | null = null;
  private latestMqttData: any = null;

  onModuleInit() {
    this.client = mqtt.connect('mqtt://localhost:1883');

    this.client.on('connect', () => {
      console.log('MQTT client connected');

      this.client?.subscribe('sensor1/data', (err) => {
        if (err) {
          console.error('MQTT subscribe error:', err);
          return;
        }

        console.log('Subscribed to sensor1/data');
      });
    });

    this.client.on('message', (topic, message) => {
      console.log('MQTT topic:', topic);
      console.log('MQTT raw message:', message.toString());

      try {
        const parsed = JSON.parse(message.toString());
        console.log('MQTT parsed message:', parsed);
        this.latestMqttData = parsed;
      } catch (error) {
        console.error('JSON parse error:', error);
        this.latestMqttData = {
          raw: message.toString(),
          topic,
        };
      }
    });

    this.client.on('error', (err) => {
      console.error('MQTT client error:', err);
    });
  }

  onModuleDestroy() {
    this.client?.end();
  }

  getLatestMqttData() {
    console.log('Returning latest MQTT data:', this.latestMqttData);
    return this.latestMqttData;
  }
}