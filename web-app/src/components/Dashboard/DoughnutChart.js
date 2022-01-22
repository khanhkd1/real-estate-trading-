import {Doughnut} from '../Charts/BaseCharts'
import _ from 'lodash'

export default {
    extends: Doughnut,
    props: ['labels', 'data'],
    mounted() {
        this.renderChart({
            labels: ['Doanh Thu', 'Lợi Nhuận',],
            datasets: [
                {
                    backgroundColor: [
                        '#ff6384',
                        '#4bc0c0'
                    ],
                    data: this.data
                }
            ],
        }, {
            responsive: true,
            maintainAspectRatio: false,
            tooltips: {
                callbacks: {
                    label(tooltipItem, data) {
                        let index = _.get(tooltipItem, 'index', 0);
                        let value = _.get(data, 'datasets[0].data[' + index + ']', 0)
                        let label = _.get(data, 'labels[' + index + ']', 'Doanh số')
                        value = value.toString()
                        value = value.split(/(?=(?:...)*$)/);
                        value = value.join(',');
                        return label + ': ' + value + ' đ';
                    }
                }
            }
        })
    },
    watch: {
        data() {
            this.renderChart({
                labels: ['Doanh Thu', 'Lợi Nhuận',],
                datasets: [
                    {
                        backgroundColor: [
                            '#ff6384',
                            '#4bc0c0'
                        ],
                        data: this.data
                    }
                ]
            }, {
                responsive: true,
                maintainAspectRatio: false,
                tooltips: {
                    callbacks: {
                        label(tooltipItem, data) {
                            let index = _.get(tooltipItem, 'index', 0);
                            let value = _.get(data, 'datasets[0].data[' + index + ']', 0)
                            let label = _.get(data, 'labels[' + index + ']', 'Doanh số')
                            value = value.toString()
                            value = value.split(/(?=(?:...)*$)/);
                            value = value.join(',');
                            return label + ': ' + value + ' đ';
                        }
                    }
                }
            })
        }
    }
}
