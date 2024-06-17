class Services {
    static async get(address, params,
                     successCallback = () => {
                     },
                     errorCallback = () => {
                     }) {
        const response = await axios({
            url: address,
            headers: {'Authorization': `Token ${CONTEXT.AUTH_TOKEN}`},
            method: 'get',
            params,
        })
        if (response.status === 200) {
            successCallback(response.data)
        }
        errorCallback()
    }


    static async post(address, payload,
                      successCallback = () => {
                      },
                      errorCallback = () => {
                      }) {
        try {
            const response = await axios({
                headers: {'Authorization': `Token ${CONTEXT.AUTH_TOKEN}`},
                url: address,
                method: 'post',
                datatype: 'json',
                data: {...payload, csrfmiddlewaretoken: CONTEXT.CSRF_TOKEN},
            })
            if (response.status === 201 || response.status===200) {
                successCallback(response.data)
            } else {
                errorCallback()
            }
        } catch (e) {
            errorCallback()
        }

    }


    static async put(address, payload,
                     successCallback = () => {
                     },
                     errorCallback = () => {
                     }) {
        const response = await axios({
            headers: {'Authorization': `Token ${CONTEXT.AUTH_TOKEN}`},
            url: address,
            method: 'put',
            datatype: 'json',
            data: {...payload, csrfmiddlewaretoken: CONTEXT.CSRF_TOKEN},
        })
        if (response.status === 200) {
            successCallback(response.data)
        } else {
            errorCallback()
        }
    }

    static async patch(address, payload,
                     successCallback = () => {
                     },
                     errorCallback = () => {
                     }) {
        const response = await axios({
            headers: {'Authorization': `Token ${CONTEXT.AUTH_TOKEN}`},
            url: address,
            method: 'patch',
            datatype: 'json',
            data: {...payload, csrfmiddlewaretoken: CONTEXT.CSRF_TOKEN},
        })
        if (response.status === 200) {
            successCallback(response.data)
        } else {
            errorCallback()
        }
    }
    static async delete(address,
                     successCallback = () => {
                     },
                     errorCallback = () => {
                     }) {
        const response = await axios({
            url: address,
            headers: {'Authorization': `Token ${CONTEXT.AUTH_TOKEN}`},
            method: 'delete',
        })
        if (response.status === 204) {
            successCallback(response.data)
        }
        errorCallback()
    }
}
