const { atlassianEndpoints, getAppNames, reportIncident, getCustomEndpoints, addApp, getStatus } = require("./services/healthCheck");

const healthHandler = async event => {

		try{

			if (event.httpMethod == "GET") {
				return atlassianEndpoints();
			}else if(event.httpMethod == "POST"){

				const data = JSON.parse(event.body);

				switch(data.action){
					case "getAppNames":
					 const names = await getAppNames();
					 return names;
					case "addApp":
					 return addApp(data);
					case "reportIncident":
					 return reportIncident(data);
					case "customFeed":
					 return getCustomEndpoints(data);
					case "getStatus":
					 return getStatus(data);
					default:
					 throw { message: "invalid method"};
				}
			}else {
			throw { message: "invalid method"};
		}
		}catch(err){
			return err;
		}
	};

module.exports = {
	healthHandler
};
