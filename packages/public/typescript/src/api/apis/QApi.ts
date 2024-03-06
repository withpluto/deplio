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


import * as runtime from '../runtime';
import type {
  ErrorResponse,
  GetQMessagesResponse,
  HTTPValidationError,
  Messages,
  PostQMessagesResponse,
} from '../models/index';
import {
    ErrorResponseFromJSON,
    ErrorResponseToJSON,
    GetQMessagesResponseFromJSON,
    GetQMessagesResponseToJSON,
    HTTPValidationErrorFromJSON,
    HTTPValidationErrorToJSON,
    MessagesFromJSON,
    MessagesToJSON,
    PostQMessagesResponseFromJSON,
    PostQMessagesResponseToJSON,
} from '../models/index';

export interface QApiListRequest {
    page?: number;
    page_size?: number;
    deplio_version?: Date;
}

export interface QApiSendRequest {
    messages: Messages;
    deplio_version?: Date;
}

/**
 * 
 */
export class QApi extends runtime.BaseAPI {

    /**
     * Get a list of messages that have been sent to Deplio Q and their responses (if any).
     * List Deplio Q messages
     */
    async listRaw(requestParameters: QApiListRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<GetQMessagesResponse>> {
        const queryParameters: any = {};

        if (requestParameters.page !== undefined) {
            queryParameters['page'] = requestParameters.page;
        }

        if (requestParameters.page_size !== undefined) {
            queryParameters['page_size'] = requestParameters.page_size;
        }

        const headerParameters: runtime.HTTPHeaders = {};

        if (requestParameters.deplio_version !== undefined && requestParameters.deplio_version !== null) {
            headerParameters['deplio-version'] = String(requestParameters.deplio_version);
        }

        if (this.configuration && this.configuration.accessToken) {
            const token = this.configuration.accessToken;
            const tokenString = await token("HTTPBearer", []);

            if (tokenString) {
                headerParameters["Authorization"] = `Bearer ${tokenString}`;
            }
        }
        const response = await this.request({
            path: `/q`,
            method: 'GET',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => GetQMessagesResponseFromJSON(jsonValue));
    }

    /**
     * Get a list of messages that have been sent to Deplio Q and their responses (if any).
     * List Deplio Q messages
     */
    async list(requestParameters: QApiListRequest = {}, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<GetQMessagesResponse> {
        const response = await this.listRaw(requestParameters, initOverrides);
        return await response.value();
    }

    /**
     * Send messages to Deplio Q to be processed asynchronously.
     * Send messages to Deplio Q
     */
    async sendRaw(requestParameters: QApiSendRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<runtime.ApiResponse<PostQMessagesResponse>> {
        if (requestParameters.messages === null || requestParameters.messages === undefined) {
            throw new runtime.RequiredError('messages','Required parameter requestParameters.messages was null or undefined when calling send.');
        }

        const queryParameters: any = {};

        if (requestParameters.messages !== undefined) {
            queryParameters['messages'] = requestParameters.messages;
        }

        const headerParameters: runtime.HTTPHeaders = {};

        if (requestParameters.deplio_version !== undefined && requestParameters.deplio_version !== null) {
            headerParameters['deplio-version'] = String(requestParameters.deplio_version);
        }

        if (this.configuration && this.configuration.accessToken) {
            const token = this.configuration.accessToken;
            const tokenString = await token("HTTPBearer", []);

            if (tokenString) {
                headerParameters["Authorization"] = `Bearer ${tokenString}`;
            }
        }
        const response = await this.request({
            path: `/q`,
            method: 'POST',
            headers: headerParameters,
            query: queryParameters,
        }, initOverrides);

        return new runtime.JSONApiResponse(response, (jsonValue) => PostQMessagesResponseFromJSON(jsonValue));
    }

    /**
     * Send messages to Deplio Q to be processed asynchronously.
     * Send messages to Deplio Q
     */
    async send(requestParameters: QApiSendRequest, initOverrides?: RequestInit | runtime.InitOverrideFunction): Promise<PostQMessagesResponse> {
        const response = await this.sendRaw(requestParameters, initOverrides);
        return await response.value();
    }

}
