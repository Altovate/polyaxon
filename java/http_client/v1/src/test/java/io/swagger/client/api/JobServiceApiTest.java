// Copyright 2019 Polyaxon, Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/*
 * Polyaxon sdk
 * No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)
 *
 * OpenAPI spec version: 1.14.4
 * Contact: contact@polyaxon.com
 *
 * NOTE: This class is auto generated by the swagger code generator program.
 * https://github.com/swagger-api/swagger-codegen.git
 * Do not edit the class manually.
 */


package io.swagger.client.api;

import io.swagger.client.ApiException;
import io.swagger.client.model.V1CodeReference;
import io.swagger.client.model.V1CodeReferenceBodyRequest;
import io.swagger.client.model.V1EntityStatusRequest;
import io.swagger.client.model.V1Job;
import io.swagger.client.model.V1JobBodyRequest;
import io.swagger.client.model.V1JobStatus;
import io.swagger.client.model.V1ListJobStatusesResponse;
import io.swagger.client.model.V1ListJobsResponse;
import io.swagger.client.model.V1OwnedEntityIdRequest;
import io.swagger.client.model.V1ProjectBodyRequest;
import org.junit.Test;
import org.junit.Ignore;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * API tests for JobServiceApi
 */
@Ignore
public class JobServiceApiTest {

    private final JobServiceApi api = new JobServiceApi();

    
    /**
     * Restore build
     *
     * 
     *
     * @throws ApiException
     *          if the Api call fails
     */
    @Test
    public void archiveJobTest() throws ApiException {
        String owner = null;
        String project = null;
        String id = null;
        Object response = api.archiveJob(owner, project, id);

        // TODO: test validations
    }
    
    /**
     * UnBookmark build
     *
     * 
     *
     * @throws ApiException
     *          if the Api call fails
     */
    @Test
    public void bookmarkJobTest() throws ApiException {
        String owner = null;
        String project = null;
        String id = null;
        Object response = api.bookmarkJob(owner, project, id);

        // TODO: test validations
    }
    
    /**
     * Create new build
     *
     * 
     *
     * @throws ApiException
     *          if the Api call fails
     */
    @Test
    public void createJobTest() throws ApiException {
        String owner = null;
        String project = null;
        V1JobBodyRequest body = null;
        V1Job response = api.createJob(owner, project, body);

        // TODO: test validations
    }
    
    /**
     * Get job code ref
     *
     * 
     *
     * @throws ApiException
     *          if the Api call fails
     */
    @Test
    public void createJobCodeRefTest() throws ApiException {
        String entityOwner = null;
        String entityProject = null;
        String entityId = null;
        V1CodeReferenceBodyRequest body = null;
        V1CodeReference response = api.createJobCodeRef(entityOwner, entityProject, entityId, body);

        // TODO: test validations
    }
    
    /**
     * Get build code ref
     *
     * 
     *
     * @throws ApiException
     *          if the Api call fails
     */
    @Test
    public void createJobStatusTest() throws ApiException {
        String owner = null;
        String project = null;
        String id = null;
        V1EntityStatusRequest body = null;
        V1JobStatus response = api.createJobStatus(owner, project, id, body);

        // TODO: test validations
    }
    
    /**
     * Delete build
     *
     * 
     *
     * @throws ApiException
     *          if the Api call fails
     */
    @Test
    public void deleteJobTest() throws ApiException {
        String owner = null;
        String project = null;
        String id = null;
        Object response = api.deleteJob(owner, project, id);

        // TODO: test validations
    }
    
    /**
     * Delete builds
     *
     * 
     *
     * @throws ApiException
     *          if the Api call fails
     */
    @Test
    public void deleteJobsTest() throws ApiException {
        String owner = null;
        String project = null;
        V1OwnedEntityIdRequest body = null;
        Object response = api.deleteJobs(owner, project, body);

        // TODO: test validations
    }
    
    /**
     * Get build
     *
     * 
     *
     * @throws ApiException
     *          if the Api call fails
     */
    @Test
    public void getJobTest() throws ApiException {
        String owner = null;
        String project = null;
        String id = null;
        V1Job response = api.getJob(owner, project, id);

        // TODO: test validations
    }
    
    /**
     * Create build code ref
     *
     * 
     *
     * @throws ApiException
     *          if the Api call fails
     */
    @Test
    public void getJobCodeRefTest() throws ApiException {
        String owner = null;
        String project = null;
        String id = null;
        V1CodeReference response = api.getJobCodeRef(owner, project, id);

        // TODO: test validations
    }
    
    /**
     * List archived builds
     *
     * 
     *
     * @throws ApiException
     *          if the Api call fails
     */
    @Test
    public void listArchivedJobsTest() throws ApiException {
        String owner = null;
        V1ListJobsResponse response = api.listArchivedJobs(owner);

        // TODO: test validations
    }
    
    /**
     * List bookmarked builds
     *
     * 
     *
     * @throws ApiException
     *          if the Api call fails
     */
    @Test
    public void listBookmarkedJobsTest() throws ApiException {
        String owner = null;
        V1ListJobsResponse response = api.listBookmarkedJobs(owner);

        // TODO: test validations
    }
    
    /**
     * Create new build status
     *
     * 
     *
     * @throws ApiException
     *          if the Api call fails
     */
    @Test
    public void listJobStatusesTest() throws ApiException {
        String owner = null;
        String project = null;
        String id = null;
        V1ListJobStatusesResponse response = api.listJobStatuses(owner, project, id);

        // TODO: test validations
    }
    
    /**
     * List builds
     *
     * 
     *
     * @throws ApiException
     *          if the Api call fails
     */
    @Test
    public void listJobsTest() throws ApiException {
        String owner = null;
        String project = null;
        V1ListJobsResponse response = api.listJobs(owner, project);

        // TODO: test validations
    }
    
    /**
     * Patch build
     *
     * 
     *
     * @throws ApiException
     *          if the Api call fails
     */
    @Test
    public void patchJobTest() throws ApiException {
        String owner = null;
        String project = null;
        String jobId = null;
        V1JobBodyRequest body = null;
        V1Job response = api.patchJob(owner, project, jobId, body);

        // TODO: test validations
    }
    
    /**
     * Restart build
     *
     * 
     *
     * @throws ApiException
     *          if the Api call fails
     */
    @Test
    public void restartJobTest() throws ApiException {
        String owner = null;
        String project = null;
        String id = null;
        V1OwnedEntityIdRequest body = null;
        V1Job response = api.restartJob(owner, project, id, body);

        // TODO: test validations
    }
    
    /**
     * Bookmark build
     *
     * 
     *
     * @throws ApiException
     *          if the Api call fails
     */
    @Test
    public void restoreJobTest() throws ApiException {
        String owner = null;
        String project = null;
        String id = null;
        Object response = api.restoreJob(owner, project, id);

        // TODO: test validations
    }
    
    /**
     * Archive build
     *
     * 
     *
     * @throws ApiException
     *          if the Api call fails
     */
    @Test
    public void resumeJobTest() throws ApiException {
        String owner = null;
        String project = null;
        String id = null;
        V1OwnedEntityIdRequest body = null;
        V1Job response = api.resumeJob(owner, project, id, body);

        // TODO: test validations
    }
    
    /**
     * Stop build
     *
     * 
     *
     * @throws ApiException
     *          if the Api call fails
     */
    @Test
    public void stopJobTest() throws ApiException {
        String owner = null;
        String project = null;
        String id = null;
        V1OwnedEntityIdRequest body = null;
        Object response = api.stopJob(owner, project, id, body);

        // TODO: test validations
    }
    
    /**
     * Stop builds
     *
     * 
     *
     * @throws ApiException
     *          if the Api call fails
     */
    @Test
    public void stopJobsTest() throws ApiException {
        String owner = null;
        String project = null;
        V1ProjectBodyRequest body = null;
        Object response = api.stopJobs(owner, project, body);

        // TODO: test validations
    }
    
    /**
     * Get build status
     *
     * 
     *
     * @throws ApiException
     *          if the Api call fails
     */
    @Test
    public void unBookmarkJobTest() throws ApiException {
        String owner = null;
        String project = null;
        String id = null;
        Object response = api.unBookmarkJob(owner, project, id);

        // TODO: test validations
    }
    
    /**
     * Update build
     *
     * 
     *
     * @throws ApiException
     *          if the Api call fails
     */
    @Test
    public void updateJobTest() throws ApiException {
        String owner = null;
        String project = null;
        String jobId = null;
        V1JobBodyRequest body = null;
        V1Job response = api.updateJob(owner, project, jobId, body);

        // TODO: test validations
    }
    
}
