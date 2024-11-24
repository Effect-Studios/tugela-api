import json
import logging

from django.conf import settings
from openai import OpenAI
from rest_framework.exceptions import ValidationError

# openai.api_key = settings.OPEN_AI_KEY
openai_key = settings.OPEN_AI_KEY
client = OpenAI(api_key=openai_key)


JOB_ANALYSIS_PROMPT = """
    Given the following inputs:

    Candidate Profile: A detailed description of the candidate's work experience,
    technical skills, achievements, and behavioral traits.

    Job Description: A detailed outline of the job requirements,
    necessary skills, desired experience, and information about company culture and values.

    Please evaluate and score the candidate across three categories (Technical Skills and Competency,
    Cultural Fit and Behavioral Traits, and Experience and Potential), based on a 0-5 scale.
    Use the following guidelines for each score:

    Technical Skills and Competency:
    Assess the alignment of the candidate’s technical skills with those required in the job description.

    Cultural Fit and Behavioral Traits:
    Consider how well the candidate’s values, work style, and personality might fit with the
    company’s culture and team dynamics. If there is not much information about these traits,
    give the candidate a score of 2.5 in this area.

    Experience and Potential:
    Evaluate the relevance and depth of the candidate's past experiences in relation to the job role,
    as well as their potential for growth in the position.

    After scoring each category, calculate the confidence_score as the average of these scores.

    Output Format:

    The output should be a JSON object in the following format:

    {
        "Technical Skills and Competency": <score from 0-5>,
        "Cultural Fit and Behavioral Traits": <score from 0-5>,
        "Experience and Potential": <score from 0-5>,
        "confidence_score": <average of the scores above>
        "explanation": (a brief explanation of why this score was given)
        "Probability of Job Success":  (percentage value based on confidence_score)
    }

"""


def get_job_score_json(freelancer_skills, job_description):
    # Define the prompt for JSON response
    prompt = f"""
    Rate the suitability of a job for a freelancer based on the freelancer's skills and the job description.

    Freelancer's Skills:
    {freelancer_skills}

    Job Description:
    {job_description}

    Respond in JSON format with two fields:
    {{
        "score": (a number between 0 and 5 indicating the suitability),
        "technical_skills_and_competency": <score from 0-5>,
        "cultural_fit_and_behavioral_traits": <score from 0-5>,
        "experience_and_potential": <score from 0-5>,
        "confidence_score": <average of the scores above>,
        "explanation": (a brief explanation of why this score was given)
        "probability_of_job_success":  (percentage value based on confidence_score)
    }}

    JSON Response:
    """

    messages = [
        {"role": "system", "content": JOB_ANALYSIS_PROMPT},
        {"role": "user", "content": prompt},
    ]

    try:
        # Make the API call to OpenAI to generate the response
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # or "gpt-4" or "text-davinci-003" or "gpt-3.5-turbo"
            messages=messages,
            # max_tokens=100,  # Limit tokens to ensure we stay within JSON response range
            temperature=0,  # Low temperature for consistency
            response_format={"type": "json_object"},
        )
        raw_response = response.choices[0].message.content.strip()
    except Exception as e:
        logging.warning(e)
        raise ValidationError({"message": e})

    # Parse the response as JSON
    try:
        # Attempt to parse the model's response as JSON
        job_score_json = json.loads(raw_response)
        return job_score_json
    except json.JSONDecodeError:
        # Handle JSON decoding errors gracefully
        job_score_json = {"score": None, "explanation": "Could not parse JSON response"}
        logging.warning(job_description)
        raise ValidationError(job_score_json)
