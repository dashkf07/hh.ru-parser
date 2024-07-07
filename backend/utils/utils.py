def filter_vacancies(vacancies, salary_range=None, experience_range=None, city=None, company=None):
    filtered_vacancies = []

    for vacancy in vacancies:

        salary_match = True
        experience_match = False
        company_match = False
        city_match = False

        if experience_match == None:
            experience_match = True

        if salary_range == None:
            salary_match = True

        if city == None:
            city_match = True

        if company == None:
            company_match = True


        if salary_range:
            min_salary, max_salary = salary_range
            vacancy_min_salary, vacancy_max_salary = vacancy['salary']['salary']
            if not (vacancy_min_salary <= max_salary and (vacancy_max_salary >= min_salary or vacancy_max_salary == 0)):
                salary_match = False


        if experience_range:
            min_experience, max_experience = experience_range
            print(experience_range)
            print(vacancy['experience'])
            if vacancy['experience'][0] == 6 and min_experience == 6:
                experience_match = True
            elif vacancy['experience'][0] == 0 and min_experience == 0:
                experience_match = True
            elif vacancy['experience'][0] == min_experience and vacancy['experience'][1] == max_experience:
                experience_match = True
                print(vacancy['experience'][0] == min_experience)
                print(vacancy['experience'][1] == max_experience)


        if city and city.lower() != vacancy['city'].lower():
            city_match = True


        if company and company.lower() != vacancy['company'].lower():
            company_match = True

        if salary_match and experience_match and company_match and city_match:
            filtered_vacancies.append(vacancy)

    return filtered_vacancies
