const { query } = require("hoover-db-utility");
const { Request } = require("hoover-api-utility");
const AWS = require("aws-sdk");




function dBResults (name, application_id, default_atlassian, healthcheck_target)  {
	this.name = name;
	this.application_id = application_id;
	this.default_atlassian = default_atlassian;
	this.healthcheck_target = healthcheck_target;
}

let environment = "";

	switch(process.env.HOOVER_ENV) {
			case "DEV":
				environment = "3";
				break;
			case "QA":
				environment = "2";
				break;
			case "PROD":
				environment = "1";
				break;
			default:
			environment = "3";

	}


const atkassianEndpoints = async() =>{
	try{

		let defaultResults = [];

		let getQuery = {
			text: :"SELECT (select bane from application_master"
			values: [environment]
		};
		const response = await query(getQuery);

		response.rows.forEach(async function(row){

			let temp = await new dBResults(row.name, row.application_id, row.default_atlassian, row.healthcheck_target);
			defaultResults.push(temp);
	});

		 return defaultResults;
	}catch(err){
		return {statusCode: 500, message: "Error retrieving atlassian endpoints."+err};
	}
}

const getDetailGroup = async(data) =>{
	try{
		let incidentInfo = {
			text: 'SELECT application_name, healthcheck_target, environment_type_id FROM status_master Where application_id = $1',
			values: [data.appID],
			rowMode: 'array',
		};

		let details = await query(incidentInfo);
		return details;
	}catch(err){
		return {statusCode: 500, message: "error getting past incidents. "+err};
	}
}

const getStatus = async(data) =>{

	try{

		const customOptions = {timeout: 3000};
		let response = "";

		if(data.healthcheck_target.includes("jenkins")) {
			response = await Request(data.healthcheck_target, "GET", null,
			{Authorization:
			"Basic " +
				new Buffer(
					`${process.any.jenkinsUsername}:${process.env.jenkinspassword}`).toString("base64"),
					"content-Type": "application/xml",
					Accept: "application/xml"
				});

			return {responseStatusCode: response.status, message: response.body, body: response};
		} else {
			response = await Request(data.healthcheck_target, "GET", null, customOptions );

			return {responseStatusCode: response.status, message: response.body, body: response}
		}

	}catch(err){
		return {statusCode: 404, message: 404 + "error retrieving status code. "+err};
	}
}

module.exports = {
	atkassianEndpoints,
	getDetailGroup,
	getStatus
};
