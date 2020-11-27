import requests
# process.env["NODE_TLS_REJECT_UNAUTHORIZED"] = 0; need to set after

commonHeaders = {
    "Content-Type" : "application/json",
    "Accept" : "application/json",
    "Access-Control-Allow-Origin" : "*",
    "Access-Control-Allow-Origin-Credentials" : "true",
    "Access-Control-Allow-Origin-Methods": "DELETE, POST GET OPTIONS",
    "Access-Control-Allow-Origin-Headers": "Access-Control-Allow-Origin.Content-Type, Access-Control-Allow-Headers, Authorization, X-requested-With, Accet, Access-Control-Allow-Origin-Credentials"
}

commonOptions = {
    "Content-Type" : "application/json",
    "Accept" : "application/json"
}
