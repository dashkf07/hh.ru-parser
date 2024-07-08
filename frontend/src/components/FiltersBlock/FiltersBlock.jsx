import React from 'react';
import styles from './FiltersBlock.module.css';
import { useState } from 'react';
import { getFilteredVacancies, getMoreFilteredVacancies } from '../../utils/requests';

export function FiltersBlock({handleVacancies, keywords, handleUrl, url, handleType, type}) {

    const [salaryRange, setSalaryRange] = useState()
    const [experienceRange, setExperienceRange] = useState()
    const [city, setCity] = useState()
    const [company, setCompany] = useState()

    async function getVacancies() {
        const data = await getFilteredVacancies(salaryRange, experienceRange, city, company, keywords)
        handleVacancies(data.vacancies_data)
        handleUrl(data.url)
        handleType('filtered')
    }

    async function getMoreVacanciesData() {
        console.log('click')
        const data = await getMoreFilteredVacancies(salaryRange, experienceRange, city, company, url)
  
        handleVacancies(data.vacancies_data)
        handleUrl(data.url)
        handleType('filtered')
      }


    return (
        <div className={styles.filtersBlock}>
            <div className={styles.filterSection}>
                <p className={styles.filterTitle}>Диапазон зарплаты</p>
                <div className={styles.salaryRange}>
                    <input className={styles.inputSalary} type="number" placeholder="от" />
                    <input className={styles.inputSalary} type="number" placeholder="до" />
                </div>
            </div>
            
            <div className={styles.filterSection}>
                <p className={styles.filterTitle}>Опыт работы</p>
                <div className={styles.experienceOptions}>
                    <div className={styles.experienceOption}>
                        <input type="radio" name='experience' onChange={(event) => event.target.value == 'on' ? setExperienceRange([0, 0]) : setExperienceRange()}/>
                        <p>Без опыта</p>
                    </div>
                    <div className={styles.experienceOption}>
                        <input type="radio" name='experience' onChange={(event) => event.target.value == 'on' ? setExperienceRange([1, 3]) : setExperienceRange()} />
                        <p>1-3 года</p>
                    </div>
                    <div className={styles.experienceOption}>
                        <input type="radio" name='experience' onChange={(event) => event.target.value == 'on' ? setExperienceRange([3, 6]) : setExperienceRange()}/>
                        <p>3-6 лет</p>
                    </div>
                    <div className={styles.experienceOption}>
                        <input type="radio" name='experience' onChange={(event) => event.target.value == 'on' ? setExperienceRange([6, 100]) : setExperienceRange()}/>
                        <p>более 6-ти лет</p>
                    </div>
                </div>
            </div>

            <div className={styles.filterSection}>
                <p className={styles.filterTitle}>Компания</p>
                <input className={styles.inputCompany} type="text" placeholder="Введите название компании" />
            </div>

            <div className={styles.filterSection}>
                <p className={styles.filterTitle}>Город</p>
                <input className={styles.inputCity} type="text" placeholder="Введите название города" />
            </div>
            <div>
                <button className={styles.button}  onClick={() => getVacancies()}>Получить вакансии</button>
            </div>

            {
                type == 'filtered' &&  <button className={styles.button} onClick={() => getMoreVacanciesData()}>Получить еще вакансии</button>
            }
        </div>
    );
}
