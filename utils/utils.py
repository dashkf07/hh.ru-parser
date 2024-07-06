def filter_vacancies(vacancies, min_salary=None, max_salary=None, min_experience=None, max_experience=None, company=None, city=None):
    def matches_salary(vacancy, min_salary, max_salary):
        if min_salary is None and max_salary is None:
            return True
        salary_info = vacancy['salary']['salary']
        if not salary_info or salary_info == [None]:
            return False
        min_vacancy_salary = salary_info[0]
        max_vacancy_salary = salary_info[-1] if len(salary_info) > 1 else min_vacancy_salary
        if min_salary is not None and max_vacancy_salary < min_salary:
            return False
        if max_salary is not None and min_vacancy_salary > max_salary:
            return False
        return True

    def matches_experience(vacancy, min_experience, max_experience):
        exp_info = vacancy['experience']
        min_vacancy_exp = exp_info[0] if exp_info and exp_info != [None] else None
        max_vacancy_exp = exp_info[1] if len(exp_info) > 1 else min_vacancy_exp
        if min_experience is not None:
            if min_vacancy_exp is None or min_vacancy_exp > min_experience:
                return False
        if max_experience is not None:
            if max_vacancy_exp is None or max_vacancy_exp < max_experience:
                return False
        return True

    def matches_company(vacancy, company):
        if company is None:
            return True
        return vacancy['company'].lower() == company.lower()

    def matches_city(vacancy, city):
        if city is None:
            return True
        return vacancy['city'].lower() == city.lower()

    filtered_vacancies = []
    for vacancy in vacancies:
        print(vacancy)
        if (matches_salary(vacancy, min_salary, max_salary) and
                matches_experience(vacancy, min_experience, max_experience) and
                matches_company(vacancy, company) and
                matches_city(vacancy, city)):
            print('ПОДОШЛО')
            print(vacancy)
            filtered_vacancies.append(vacancy)
    return filtered_vacancies





