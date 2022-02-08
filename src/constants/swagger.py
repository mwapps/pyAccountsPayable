template = {
    "swagger": "2.0",
    "info": {
        "title": "Accounts Payable API",
        "description": "API for our accounts payable",
        "contact": {
            "responsibleOrganization": "",
            "responsibleDeveloper": "",
            "url": "https://www.manriqueweb.com",
        },
        "termsOfService": "https://www.manriqueweb.com/privacypolicy/index.htm",
        "version": "1.0"
    },
    "basePath": "/api/v1",  # base bash for blueprint registration
    "schemes": [
        "http",
        "https"
    ],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
        }
    },
    "definitions": {
        "company": {
            "type": "object",
            "description": "Company data object representation",
            "properties":{
              "company_id":{
                "type": "integer",
                "format": "int32",
                "example": "2"
              },
              "business_name":{
                "type": "string",
                "description": "Name of the comnpany",
                "example": "Empresas Peroles SL"              
              }
            }
        },
        "supplier": {
            "type": "object",
            "description": "Supplier data object representation",
            "properties":{
              "supplier_id":{
                "type": "integer",
                "format": "int32",
                "example": "2"
              },
              "supplier_name":{
                "type": "string",
                "description": "Name of the supplier",
                "example": "Zapateria Los cien pies, SLR"              
              }
            }
        },
        "user": {
            "type": "object",
            "description": "User data object representation",
            "properties":{
              "user_id":{
                "type": "integer",
                "format": "int32",
                "example": "69"
              },
              "user_email":{
                "type": "email",
                "description": "User email",
                "example": "enrique.sido-mogollon@gmail.com"
              },
              "user_name":{
                "type": "string",
                "description": "User name",
                "example": "esidomogollo"
              }
            }
        },
        "rule": {
            "type": "object",
            "description": "Rule data object representation",
            "properties":{
              "rule_id":{
                "type": "integer",
                "format": "int32",
                "example": "10"
              },
              "rule_description":{
                "type": "string",
                "description": "Rule description",
                "example": "Purchase",
              },
              "action_over_document":{
                "type": "string",
                "description": "Action over document (Create / Update / Any)",
                "example": "C",
                "enum": ["C", "U", "A"]
              },
              "movement_type":{
                "type": "string",
                "description": "Movement type (Debit / Credit / No effect)",
                "example": "D",
                "enum": ["D", "C", "N"]
              },
              "update_issue_date":{
                "type": "string",
                "description": "Update the issue date (Yes / No)",
                "example": "Y",
                "enum": ["Y", "N"]
              },
              "update_due_date":{
                "type": "string",
                "description": "Update the due date (Yes / No)",
                "example": "Y",
                "enum": ["Y", "N"]
              },
              "update_reference":{
                "type": "string",
                "description": "Update the reference (Yes / No)",
                "example": "N",
                "enum": ["Y", "N"]
              }
            }
        },
        "amount": {
            "type": "number",
            "description": "Amount of the transaction to process",
            "example": "59.95"
        },
        "issue_date": {
            "type": "string",
            "description": "Date of issuance of document",
            "format": "YYYY-MM-DD",
            "example": "2022-01-09"
        },
        "due_date": {
            "type": "string",
            "description": "Document expiration date",
            "format": "YYYY-MM-DD",
            "example": "2022-01-09"
        },
        "movement_date": {
            "type": "string",
            "description": "The date of record the transaction",
            "format": "YYYY-MM-DD",
            "example": "2022-01-09"
        },
        "document_number": {
            "type": "string",
            "description": "Document number",
            "example": "0003"
        },
        "reference": {
            "type": "string",
            "description": "Any document number related to the document",
            "example": "OR0001"
        },
        "movement_id": {
            "type": "integer",
            "format": "int32",
            "example": "69"
        },
        "email": {
            "type": "email",
            "example": "user.name@companydomain.com"
        },
        "password": {
            "type": "string",
            "format": "password",
            "example": "*********"
        },
        "access": {
            "type": "string",
            "example": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0MTkyNjY0NSwianRpIjoiODY4OThiNDQtMTRlYy00NDNiLWJiYzQtMjE1MDE2MGE3Mzc4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6OCwibmJmIjoxNjQxOTI2NjQ1LCJleHAiOjE2NDE5MzAyNDV9.QVoruWZ1LS9fM0-HLWW59ONUDm9uUUeyfGBBgyZZzzZ",
        },
        "refresh": {
            "type": "string",
            "example": "Re0T0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY0MTkyNjY0NSwianRpIjoiODY4OThiNDQtMTRlYy00NDNiLWJiYzQtMjE1MDE2MGE3Mzc4IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6OCwibmJmIjoxNjQxOTI2NjQ1LCJleHAiOjE2NDE5MzAyNDV9.QVoruWZ1LS9fM0-HLWW59ONUDm9uUUeyfGBBgyZZzzZ",
        },
        "username": {
            "type": "string",
            "example": "heSidoMogollon",
        },
        "company_id": {
            "type": "integer",
            "format": "int32",
            "example": "69"
        },
        "supplier_id": {
            "type": "integer",
            "format": "int32",
            "example": "69"
        },
        "rule_id": {
            "type": "integer",
            "format": "int32",
            "example": "69"
        },
        "from_date": {
            "type": "string",
            "description": "Document expiration date",
            "format": "YYYY-MM-DD",
            "example": "2022-01-01"
        },
        "to_date": {
            "type": "string",
            "description": "Document expiration date",
            "format": "YYYY-MM-DD",
            "example": "2022-12-31"
        },
        "document": {
            "type": "object",
            "description": "Document data object representation",
            "properties":{
                "company": {
                    "type": "object",
                    "description": "Company data object representation",
                    "properties":{
                      "company_id":{
                        "type": "integer",
                        "format": "int32",
                        "example": "2"
                      },
                      "business_name":{
                        "type": "string",
                        "description": "Name of the comnpany",
                        "example": "Empresas Peroles SL"              
                      }
                    }
                },
                "supplier": {
                    "type": "object",
                    "description": "Supplier data object representation",
                    "properties":{
                      "supplier_id":{
                        "type": "integer",
                        "format": "int32",
                        "example": "2"
                      },
                      "supplier_name":{
                        "type": "string",
                        "description": "Name of the supplier",
                        "example": "Zapateria Los cien pies, SLR"              
                      }
                    }
                },
                "balance": {
                    "type": "number",
                    "description": "balance of documents",
                    "example": "10.00"
                },
                "previous_balance": {
                    "type": "number",
                    "description": "previous_balance of documents",
                    "example": "10.00"
                },
                "total_credits": {
                    "type": "number",
                    "description": "total_credits of documents",
                    "example": "10.00"
                },
                "total_debits": {
                    "type": "number",
                    "description": "total_debits of documents",
                    "example": "10.00"
                },
                "issue_date": {
                    "type": "string",
                    "description": "Date of issuance of document",
                    "format": "YYYY-MM-DD",
                    "example": "2022-01-09"
                },
                "due_date": {
                    "type": "string",
                    "description": "Document expiration date",
                    "format": "YYYY-MM-DD",
                    "example": "2022-01-09"
                },
                "document_number": {
                    "type": "string",
                    "description": "Document number",
                    "example": "0003"
                },
                "reference": {
                    "type": "string",
                    "description": "Any document number related to the document",
                    "example": "OR0001"
                },
            }
        },
        "error": {
            "type": "object",
            "description": "The object data contain information about error validation or another system exception",
            "properties":{
              "code":{
                "type": "string",
                "example": "100"
              },
              "message":{
                "type": "string",
                "description": "Description of error",
                "example": "The document exist, please provide new document_number"              
              }
            }
        }
    }
}

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/"
}
