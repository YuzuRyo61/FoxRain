<template>
  <div>
      <p>{{ userInfo }}</p>
  </div>
</template>

<script>
export default {
    name: 'User',
    data () {
        return {
            userInfo: null,
            isError: false
        }
    },
    mounted () {
        this.axios
            .get(`/api/user/${this.$route.params.username}`)
            .then(response => (this.userInfo = response.data))
            .catch(error => {
                console.error(error)
                this.isError = true
            })
    }
}
</script>

<style>

</style>
