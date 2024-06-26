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
import type { QRequestWithResponses } from './QRequestWithResponses';
import {
    QRequestWithResponsesFromJSON,
    QRequestWithResponsesFromJSONTyped,
    QRequestWithResponsesToJSON,
} from './QRequestWithResponses';

/**
 * 
 * @export
 * @interface GetQMessagesResponse
 */
export interface GetQMessagesResponse {
    /**
     * 
     * @type {Array<DeplioWarning>}
     * @memberof GetQMessagesResponse
     */
    warnings: Array<DeplioWarning>;
    /**
     * 
     * @type {Array<QRequestWithResponses>}
     * @memberof GetQMessagesResponse
     */
    requests: Array<QRequestWithResponses>;
    /**
     * 
     * @type {number}
     * @memberof GetQMessagesResponse
     */
    count: number;
    /**
     * 
     * @type {number}
     * @memberof GetQMessagesResponse
     */
    total: number;
    /**
     * 
     * @type {number}
     * @memberof GetQMessagesResponse
     */
    page: number;
    /**
     * 
     * @type {number}
     * @memberof GetQMessagesResponse
     */
    page_size: number;
}

/**
 * Check if a given object implements the GetQMessagesResponse interface.
 */
export function instanceOfGetQMessagesResponse(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "warnings" in value;
    isInstance = isInstance && "requests" in value;
    isInstance = isInstance && "count" in value;
    isInstance = isInstance && "total" in value;
    isInstance = isInstance && "page" in value;
    isInstance = isInstance && "page_size" in value;

    return isInstance;
}

export function GetQMessagesResponseFromJSON(json: any): GetQMessagesResponse {
    return GetQMessagesResponseFromJSONTyped(json, false);
}

export function GetQMessagesResponseFromJSONTyped(json: any, ignoreDiscriminator: boolean): GetQMessagesResponse {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'warnings': ((json['warnings'] as Array<any>).map(DeplioWarningFromJSON)),
        'requests': ((json['requests'] as Array<any>).map(QRequestWithResponsesFromJSON)),
        'count': json['count'],
        'total': json['total'],
        'page': json['page'],
        'page_size': json['page_size'],
    };
}

export function GetQMessagesResponseToJSON(value?: GetQMessagesResponse | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'warnings': ((value.warnings as Array<any>).map(DeplioWarningToJSON)),
        'requests': ((value.requests as Array<any>).map(QRequestWithResponsesToJSON)),
        'count': value.count,
        'total': value.total,
        'page': value.page,
        'page_size': value.page_size,
    };
}

