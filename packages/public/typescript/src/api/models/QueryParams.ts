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
 * @interface QueryParams
 */
export interface QueryParams {
}

/**
 * Check if a given object implements the QueryParams interface.
 */
export function instanceOfQueryParams(value: object): boolean {
    let isInstance = true;

    return isInstance;
}

export function QueryParamsFromJSON(json: any): QueryParams {
    return QueryParamsFromJSONTyped(json, false);
}

export function QueryParamsFromJSONTyped(json: any, ignoreDiscriminator: boolean): QueryParams {
    return json;
}

export function QueryParamsToJSON(value?: QueryParams | null): any {
    return value;
}
