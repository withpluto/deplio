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
 * @interface DeletedAt
 */
export interface DeletedAt {
}

/**
 * Check if a given object implements the DeletedAt interface.
 */
export function instanceOfDeletedAt(value: object): boolean {
    let isInstance = true;

    return isInstance;
}

export function DeletedAtFromJSON(json: any): DeletedAt {
    return DeletedAtFromJSONTyped(json, false);
}

export function DeletedAtFromJSONTyped(json: any, ignoreDiscriminator: boolean): DeletedAt {
    return json;
}

export function DeletedAtToJSON(value?: DeletedAt | null): any {
    return value;
}

