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
 * @interface Headers
 */
export interface Headers {
}

/**
 * Check if a given object implements the Headers interface.
 */
export function instanceOfHeaders(value: object): boolean {
    let isInstance = true;

    return isInstance;
}

export function HeadersFromJSON(json: any): Headers {
    return HeadersFromJSONTyped(json, false);
}

export function HeadersFromJSONTyped(json: any, ignoreDiscriminator: boolean): Headers {
    return json;
}

export function HeadersToJSON(value?: Headers | null): any {
    return value;
}
