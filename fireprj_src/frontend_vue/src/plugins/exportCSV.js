import _ from 'lodash'

const exportCsv = (data, filename) => {
    if (!data || !filename) return;
    const BOM = "\uFEFF"
    let csvString = BOM

    _.each(data, (row) => {
        let r = row.map(v => '"' + v.toString().replace(/"/g, '""') + '"')
        csvString += r.join(',') + '\r\n'
    })
    csvString = csvString.replace(/\r\n$/, '')

    // IE 10, 11, Edge Run
    if (window.navigator && window.navigator.msSaveOrOpenBlob) {

        let blob = new Blob([csvString], {
            type: 'text/csv;charset=utf8'
        });

        window.navigator.msSaveOrOpenBlob(blob, filename);

    } else if (window.Blob && window.URL) {
        // HTML5 Blob
        let blob = new Blob([csvString], { type: 'text/csv;charset=utf8' });
        let csvUrl = URL.createObjectURL(blob);
        let a = document.createElement('a');
        a.setAttribute('style', 'display:none');
        a.setAttribute('href', csvUrl);
        a.setAttribute('download', filename);
        document.body.appendChild(a);

        a.click()
        a.remove();
    } else {
        // Data URI
        let csvData = 'data:application/csv;charset=utf-8,' + encodeURIComponent(csvString);
        let blob = new Blob([csvString], { type: 'text/csv;charset=utf8' });
        let csvUrl = URL.createObjectURL(blob);
        let a = document.createElement('a');
        a.setAttribute('style', 'display:none');
        a.setAttribute('target', '_blank');
        a.setAttribute('href', csvData);
        a.setAttribute('download', filename);
        document.body.appendChild(a);
        a.click()
        a.remove();
    }
}

export default exportCsv