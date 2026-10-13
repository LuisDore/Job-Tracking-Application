
from .conftest import client


def test_create_application(created_application): #While Authenticated
    response , token  = created_application
    assert response.status_code == 201

def test_read_application(client, created_application, application_test): #While Authenticated
    response, token = created_application
    assert response.status_code == 201

    read_response = client.get("/applications", 
                               headers={                                   
                                "Authorization" : f"Bearer {token}"                            
                               })
    #print(read_response.json())
    #print(application_test)
    
    assert read_response.status_code == 200

    applications = read_response.json()

    assert len(applications) == 1 #Checks that there is only one Applicatioin in the returned list 

    returned_applicaiton = applications[0] #The response JSON also Contains the Application ID so cant just do "=="
    returned_applicaiton.pop("application_id") # Remove the application ID so they can be compared for the assert

    assert returned_applicaiton == application_test
    
   

def test_read_specific_application(client, created_application, application_test): #While Authenticated
    response, token = created_application
    assert response.status_code == 201

    read_response = client.get("/applications/1",  #Only Created One Application so the "application_id" should be 1
                               headers={                                   
                                "Authorization" : f"Bearer {token}"                            
                               })

    assert read_response.status_code == 200

    application = read_response.json()
    assert application.pop("application_id") == 1 #Checks if the returned "application_id" is 1

    assert application == application_test #Checks if the the returned application is the same as the one created 
    
def test_update_application(client, created_application, application_test): #While Authenticated
    response, token = created_application
    assert response.status_code == 201

    update_response = client.put("/applications/1",  #Only Created One Application so the "application_id" should be 1
                                headers={                                   
                                "Authorization" : f"Bearer {token}"                            
                                 })
    




def test_delete_application(client, register_user): #While Authenticated
    pass

def test_access_without_jwt(client, register_user): 
    pass

def test_access_nonexistant_application(client, register_user): #If user tries to access an application that doesnt exist 
    pass

def test_user_crossover(client, register_user): #If user A tries to access user b's applications
    pass