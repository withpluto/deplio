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
/**
 * 
 * @export
 * @interface QResponse
 */
export interface QResponse {
    /**
     * 
     * @type {string}
     * @memberof QResponse
     */
    id: string;
    /**
     * 
     * @type {Date}
     * @memberof QResponse
     */
    created_at: Date;
    /**
     * 
     * @type {Date}
     * @memberof QResponse
     */
    deleted_at: Date;
    /**
     * 
     * @type {string}
     * @memberof QResponse
     */
    request_id: string;
    /**
     * 
     * @type {number}
     * @memberof QResponse
     */
    status_code: number;
    /**
     * 
     * @type {string}
     * @memberof QResponse
     */
    body: string;
    /**
     * 
     * @type {{ [key: string]: string; }}
     * @memberof QResponse
     */
    headers: { [key: string]: string; };
    /**
     * 
     * @type {number}
     * @memberof QResponse
     */
    response_time_ns: number;
}

/**
 * Check if a given object implements the QResponse interface.
 */
export function instanceOfQResponse(value: object): boolean {
    let isInstance = true;
    isInstance = isInstance && "id" in value;
    isInstance = isInstance && "created_at" in value;
    isInstance = isInstance && "deleted_at" in value;
    isInstance = isInstance && "request_id" in value;
    isInstance = isInstance && "status_code" in value;
    isInstance = isInstance && "body" in value;
    isInstance = isInstance && "headers" in value;
    isInstance = isInstance && "response_time_ns" in value;

    return isInstance;
}

export function QResponseFromJSON(json: any): QResponse {
    return QResponseFromJSONTyped(json, false);
}

export function QResponseFromJSONTyped(json: any, ignoreDiscriminator: boolean): QResponse {
    if ((json === undefined) || (json === null)) {
        return json;
    }
    return {
        
        'id': json['id'],
        'created_at': (new Date(json['created_at'])),
        'deleted_at': (new Date(json['deleted_at'])),
        'request_id': json['request_id'],
        'status_code': json['status_code'],
        'body': json['body'],
        'headers': json['headers'],
        'response_time_ns': json['response_time_ns'],
    };
}

export function QResponseToJSON(value?: QResponse | null): any {
    if (value === undefined) {
        return undefined;
    }
    if (value === null) {
        return null;
    }
    return {
        
        'id': value.id,
        'created_at': (value.created_at.toISOString()),
        'deleted_at': (value.deleted_at.toISOString()),
        'request_id': value.request_id,
        'status_code': value.status_code,
        'body': value.body,
        'headers': value.headers,
        'response_time_ns': value.response_time_ns,
    };
}

