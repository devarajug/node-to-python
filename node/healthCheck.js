const { query } = require("hoover-db-utility");
const { Get } = require("hoover-api-utility");
const AWS = require("aws-sdk");


function dBResults (name, application_id, default_atlassian, environment_type_id, healthcheck_target)  {
	this.name = name;
	this.application_id = application_id;
	this.default_atlassian = default_atlassian;
	this.healthcheck_target = healthcheck_target;
	this.environment_type_id = environment_type_id;
}

// let environment = "";
//
// 	switch(process.env.HOOVER_ENV) {
// 			case "DEV":
// 				environment = "3";
// 				break;
// 			case "QA":
// 				environment = "2";
// 				break;
// 			case "PROD":
// 				environment = "1";
// 				break;
// 			default:
// 			environment = "3";
//
// 	}

// var appNames = (name) => this.name = name;

const atlassianEndpoints = async() =>{
	try{

		let defaultResults = [];

		const response = await query("SELECT (select name FROM application_master WHERE status_master.application_id = application_master.application_id), application_id, default_atlassian, environment_type_id, healthcheck_target FROM status_master WHERE default_atlassian = TRUE ORDER BY environment_type_id, name");

		response.rows.forEach(async function(row){

			let temp = await new dBResults(row.name, row.application_id, row.default_atlassian, row.environment_type_id, row.healthcheck_target);
			defaultResults.push(temp);
	});

		 return defaultResults;
	}catch(err){
		return {statusCode: 500, message: "Error retrieving atlassian endpoints."+err};
	}
}

const getInternalID= async(data) =>{

	let internalIDQuery = {
		text: "SELECT internal_id FROM user_master WHERE employee_id = $1",
		values: [data.userID]
	};

	let internalID = await query(internalIDQuery):

	return internalID;
}

const getCustomENdpoints = async(data) =>{

	try{

		let internalID = await getInternalID(data);
		let appOwner = {
			text: "SELECT DISTINCT status_id FROM application_master Where internal_id = $1",
			values: [internalID.rows[0].internal_id],
			rowMode: 'array',
		};

		let appOwnerQuery = await query(appOwner);

		if(appOwnerQuery.rows){
			let PPLIST = [];


			results.rows.forEach(element =>{
				appList = appList.concat(element[0]);
			})

			let applications = {
				text: "SELECT DISTINCT application_name, application_master.application_id, environment_type_id, healthcheck_target FROM status_master LEFT OUTER JOIN application_master ON status_master.application_id = application_master.application_id WHERE application_master.application_id = ANY (&=$1) AND default_atlassian=FALSE ORDER BY environment_type_id, application_name",
				values: [appList],
			};

			return query(applications);
		}
	}catch(err){
		return {statusCode: 500, message: "ERROR retrieving application names. " +err};
	}
}

const checkDuplicateName= async(data) =>{
	const duplicate = {
		text: "SELECT EXISTS (SELECT application_name FROM status_master WHERE application_name=$1)",
		values: [data.appName]};

	if(query(duplicate).rows[0]){
		return true;
	}else{
		return false;
	}
}

const checkDuplicateEndpoint= async(data) =>{
	let duplicate = {
		text: "SELECT EXISTS (SELECT healthcheck_target FROM status_master WHERE healthcheck_target=$1)",
		values: [data.endpoint]};

	if(query(duplicate).rows[0]){
		return true;
	}else{
		return false;
	}
}

const getAppNames= async(data) =>{
	try{
		let results = [];
		let response = await query("SELECT name from application_master ORDER BY name");

		response.rows .forEach(async function(row){
			let teno =await new appnames(row.name);
			results.push(temp);
		}).catch(err => {
			return {statusCode: 500, message: "Error retrieving appliacation names. " +err};
		});

		return results;
	}catch(err){
		return {statusCode: 500, message: "Error retrieving appliacation names. " +err};
	}
}

const subscribeuser = async(data, status_id) =>{
	let internalId = await getInternalID(data);

	let appOwnerQuery = {
		text: "INSERT INTO status_master_subscription(status_id, internal_id) VALUES($1, $2)",
		values: [status_id, internalID.rows[0].internal_id]
	};

	let insertOwner = await query(appOwnerQuery);

	return insertOwner;
}

const addApp = async(data) =>{

	let envType= "";
	if(data.environment === "PROD"){
		envType=1;
	}else if(data.environment === "UAT"){
		envType=2;
	}else{
		envType=3;
	}

	try{
		let internalID = await getInternalID(data);

		if(data.newGroup){
			//create new app group

			//create new sns topic
		}else{
			//Add app to status_master table following app group

			let appQuery = {
				text: "SELECT application_id FROM status_master WHERE name=$1)",
				values: [data.appGroup],
			};

			let appID = await query(appQuery);

			let insertQuery = {
				text: "INSERT INTO status_master(application_id, default_atlassian, environment_type_id, healthcheck_target, slack_channel, application_name) VALUES($1, $2, $3, $4, $5, $6) RETURNING status_id",
				values: [appID.rows[0].application_id, false, envType, data.endpoint, data.slack, data.appName],
			};

			let insertStatus = await query(insertQuery);

			//ADD to user subscriptions
			return subscribeUser(data, insertStatus)
		}
	}catch(err){
		return {statusCode: 500, message: "Error adding application. "+err};
	}
}

const reportIncident = async(data) =>{

	try{
		//GET APp ID
		let idQuery = {
			text: 'SELECT application_id From appliccation_master WHERE name = $1 LIMIT 1',
			values: [data.appGroup],
		};

		let getID = await query(idQuery);

		//insert incident w/ retrieved ID
		let insertQuery = {
			text: 'INSERT INTO incident_master(application_id, incident_title, incident_description, created) Values($1, $2, $3, $4) RETURNING incident_id',
			values: [parseInt(getID.rows[0].application_id), data.title, data.description, data.timestamp],
			rowMode: 'array',
		};

		let incidentOD = await query(intentQuery);

		let insertUserInfo = {
			text: 'INSERT INTO incident_ownership(incident_id, user_id, first_name, last_name, email) Values($1, $2, $3, $4, $5) RETURNING *',
			values: [parseInt(incidentID.rows[0][0]), data.userID), data.firstName, data.lastName, data.email],
			rowMode: 'array',
		};

		return query(insertUserInfo);

	}catch(err){
		return {statusCode: 500, message: "Error getting past  incidents. "+err};
	}
}


const getIncidents = async(data) =>{
	try{
		let incidentInfo = {
			text: `SELECT incident_title, incident_description, created  From incident_master WHERE created >= current_Timestamp - Interval '30' day and application_id= $1 ORDER BY created DESC` ,
			values: [data.appID],
			rowMode: 'array,'
		};

		let incidents = await query(incidentInfo);
		return incidents;
	}catch(err){
		return {statusCode: 500, message: "Error getting past  incidents. "+err};
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
		let response = await Get(data.healthcheck_target, {}, customOptions );
		return {statusCode: response.status, message: "success", body: response.body};
	}catch(err){
		return {statusCode: 404, message: "error retrieving status code. "+err};
	}
}

module.exports = {
	atkassianEndpoints,
	getAppNames,
	reportIncident,
	getCustomENdpoints,
	addApp,
	getIncidents,
	getDetailGroup,
	getStatus
};
