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
import type { DeplioWarning } from './DeplioWarning';
import {
    DeplioWarningFromJSON,
    DeplioWarningFromJSONTyped,
    DeplioWarningToJSON,
} from './DeplioWarning';

/**
 * 
 * @export
 * @interface PostQMessagesResponse
 */
export interface PostQMessagesResponse {
    /**
     * 
     * @type {Array<DeplioWarning>}
     * @memberof PostQMessagesResponse
     */
    warnings: Array<DeplioWarning>;
    /**
     * 
     * @type {Array<string>}
     * @memberof PostQMessagesResponse
     */
    request_ids: Array<string>;
    /**
     * 
     * @type {number}
     * @memberof PostQMessagesResponse
     */
    messages_delivered: number;
}

/**
 * Check if a given object implements the PostQMessagesResponse interface.
 */
export function instanceOfPostQMessagesResponse(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "warnings" in value;
    isInstance = isInstance && "request_ids" in value;
    isInstance = isInstance && "messages_delivered" in value;

    return isInstance;
}

export function PostQMessagesResponseFromJSON(json: any): PostQMessagesResponse {
    return PostQMessagesResponseFromJSONTyped(json, false);
}

export function PostQMessagesResponseFromJSONTyped(json: any, ignoreDiscriminator: boolean): PostQMessagesResponse {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'warnings': ((json['warnings'] as Array<any>).map(DeplioWarningFromJSON)),
        'request_ids': json['request_ids'],
        'messages_delivered': json['messages_delivered'],
    };
}

export function PostQMessagesResponseToJSON(value?: PostQMessagesResponse | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'warnings': ((value.warnings as Array<any>).map(DeplioWarningToJSON)),
        'request_ids': value.request_ids,
        'messages_delivered': value.messages_delivered,
    };
}

