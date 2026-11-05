from fastapi import APIRouter, Depends, HTTPException
import app.models as models
import app.schemas as schemas
from app.database import get_db
from app.dependencies import get_current_user

router = APIRouter(prefix="/applications", tags=["applications"])


@router.get("",
        response_model=list[schemas.ApplicationResponse]
        ) #Gets all applications
def read_applications(current_user = Depends(get_current_user), db = Depends(get_db)):
    applications = db.query(models.Application).filter(models.Application.user_id == current_user.user_id).all()
    return applications

@router.post("",
        response_model= schemas.ApplicationResponse,
        status_code=201) #Creates a new application
def create_application(application : schemas.ApplicationCreate,
                        current_user = Depends(get_current_user),
                        db = Depends(get_db)):

    new_application = models.Application(
        company_name= application.company_name,
        job_title= application.job_title,
        location= application.location,
        salary= application.salary,
        status= application.status,
        date_applied= application.date_applied,
        notes= application.notes,
        job_url= application.job_url,
        user_id= current_user.user_id  # Use the logged-in user's ID

    )
    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return new_application

@router.get("/{application_id}",
        response_model=schemas.ApplicationResponse) #Gets a specific application by ID
def read_application(application_id: int,
                    current_user = Depends(get_current_user),
                    db = Depends(get_db)):

    application = db.query(models.Application).filter(models.Application.application_id == application_id,
                                                      models.Application.user_id == current_user.user_id).first()

    if application is None:
        raise HTTPException(status_code=404,
                            detail="Application not found")

    return application

@router.put("/{application_id}",
        response_model=schemas.ApplicationResponse) #Updates a specific application by ID
def update_application(application_id: int,
                       update_data : schemas.ApplicationUpdate,
                       current_user = Depends(get_current_user),
                       db = Depends(get_db)):

    db_application = db.query(models.Application).filter(models.Application.application_id == application_id,
                                                      models.Application.user_id == current_user.user_id).first()

    if db_application is None:
        raise HTTPException(status_code=404,
                            detail="Application not found")

    #exclude_unset keeps only fields the client actually sent, so an explicit null is preserved
    to_update = update_data.model_dump(exclude_unset=True)

    #These columns are nullable=False in the model, so they can't be cleared
    required_fields = {"job_title", "company_name", "status"}
    for field in required_fields:
        if field in to_update and to_update[field] is None:
            raise HTTPException(status_code=422,
                                detail=f"{field} cannot be null")

    for key, value in to_update.items():
        setattr(db_application, key, value)

    db.commit()
    db.refresh(db_application)

    return db_application

@router.delete("/{application_id}") #Deletes a specific application by ID
def delete_application(application_id: int,
                       current_user = Depends(get_current_user),
                       db = Depends(get_db),
                       status_code=204):

    application = db.query(models.Application).filter(models.Application.application_id == application_id,
                                                      models.Application.user_id == current_user.user_id).first()

    if application is None:
        raise HTTPException(status_code=404, detail="Application not found")

    db.delete(application)
    db.commit()
    return {"message": f"Application with ID {application_id} deleted successfully."}
