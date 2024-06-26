/* tslint:disable */
/* eslint-disable */
/**
 * Deplio
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 2024-02-26
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */

import { exists, mapValues } from '../runtime';
import type { ModelHTTPMethod } from './ModelHTTPMethod';
import {
    ModelHTTPMethodFromJSON,
    ModelHTTPMethodFromJSONTyped,
    ModelHTTPMethodToJSON,
} from './ModelHTTPMethod';

/**
 * 
 * @export
 * @interface Messages
 */
export interface Messages {
    /**
     * 
     * @type {string}
     * @memberof Messages
     */
    destination: string;
    /**
     * 
     * @type {string}
     * @memberof Messages
     */
    body?: string;
    /**
     * 
     * @type {ModelHTTPMethod}
     * @memberof Messages
     */
    method: ModelHTTPMethod;
    /**
     * 
     * @type {{ [key: string]: string; }}
     * @memberof Messages
     */
    headers?: { [key: string]: string; };
}

/**
 * Check if a given object implements the Messages interface.
 */
export function instanceOfMessages(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "destination" in value;
    isInstance = isInstance && "method" in value;

    return isInstance;
}

export function MessagesFromJSON(json: any): Messages {
    return MessagesFromJSONTyped(json, false);
}

export function MessagesFromJSONTyped(json: any, ignoreDiscriminator: boolean): Messages {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'destination': json['destination'],
        'body': !exists(json, 'body') ? undefined : json['body'],
        'method': ModelHTTPMethodFromJSON(json['method']),
        'headers': !exists(json, 'headers') ? undefined : json['headers'],
    };
}

export function MessagesToJSON(value?: Messages | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'destination': value.destination,
        'body': value.body,
        'method': ModelHTTPMethodToJSON(value.method),
        'headers': value.headers,
    };
}

