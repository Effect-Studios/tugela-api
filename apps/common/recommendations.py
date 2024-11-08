###########################
# Job Recommendation Engine
###########################
def recommendations(oai_key, candidate_profile, job_profile):

    import ast
    import json
    import logging

    logger = logging



    ####################
    # Construct Prompts
    ####################
    JOB_ANALYSIS_PROMPT = """
    Given the following inputs:

    Candidate Profile: A detailed description of the candidate's work experience, technical skills, achievements, and behavioral traits.

    Job Description: A detailed outline of the job requirements, necessary skills, desired experience, and information about company culture and values.

    Please evaluate and score the candidate across three categories (Technical Skills and Competency, Cultural Fit and Behavioral Traits, and Experience and Potential), based on a 0-5 scale. Use the following guidelines for each score:

    Technical Skills and Competency: Assess the alignment of the candidate’s technical skills with those required in the job description.
    Cultural Fit and Behavioral Traits: Consider how well the candidate’s values, work style, and personality might fit with the company’s culture and team dynamics. If there is not much information about these traits, give the candidate a score of 2.5 in this area.
    Experience and Potential: Evaluate the relevance and depth of the candidate's past experiences in relation to the job role, as well as their potential for growth in the position.
    After scoring each category, calculate the confidence_score as the average of these scores.

    Output Format:

    The output should be a JSON object in the following format:

    {
        "Technical Skills and Competency": <score from 0-5>,
        "Cultural Fit and Behavioral Traits": <score from 0-5>,
        "Experience and Potential": <score from 0-5>,
        "confidence_score": <average of the scores above>
    }
    
    """


    try:
        job_analysis_message = """
        Below is the information you should use to create the confidence score of the candidate's probability of successfuly completing the task. 

        Candidate's profile information:
        {0}

        Below is the job description that the client is being compared against:
        {1}
        """.format(candidate_profile, job_profile)
    except Exception as error:
        logger.error("ERROR CREATING JOB ANALYSIS MESSAGE: {0}".format(error))


    messages = [
        {
          "role": "system",
          "content": [
            {
              "type": "text",
              "text": JOB_ANALYSIS_PROMPT
            }
          ]
        },
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": job_analysis_message
            }
          ]
        }
      ]


    #########################
    # LLM Call
    #########################
    from openai import OpenAI
    client = OpenAI(api_key=oai_key)

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )
        
        try:
            job_recruiter_response = dict(completion.choices[0].message)["content"]
        except Exception as error:
            job_recruiter_response = ast.literal_eval(completion.choices[0].message.content.replace("```","").replace("\n","").replace("json",""))
        
        else:
            
            try:
                job_recruiter_response = ast.literal_eval(job_recruiter_response)
            except Exception as error:
                job_recruiter_response = json.loads(job_recruiter_response)
                
        job_recruiter_response["probability_of_job_success"] = 100 * float(job_recruiter_response["confidence_score"]) / 5

    except Exception as error:
        job_recruiter_response = {'Technical Skills and Competency': 3.2}
        job_recruiter_response = {'Cultural Fit and Behavioral Traits': 3.2}
        job_recruiter_response = {'Experience and Potential': 3.2}
        job_recruiter_response = {"confidence_score": 3.2}
        job_recruiter_response["probability_of_job_success"] = 100 * job_recruiter_response["confidence_score"] / 5
        logger.error("OAI ENDPOINT CALL FAILURE: {0} | USE SKILLS MATCH INSTEAD".format(error))
        
    return job_recruiter_response