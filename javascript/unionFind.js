class unionFind {
    constructor(N) {
        this.parent = [];
        this.rank = [];
        this.groupCount = N;
        for (let i=0; i < N; i++) {
            this.parent.push(i);
            this.rank.push(0);
        }
    }

    find(x) {
        if (this.parent[x] === x) {
            return x;
        } else {
            let result = this.find(this.parent[x]);
            this.parent[x] = result;
            return result;
        }
    }

    unite(x, y) {
        x = this.find(x);
        y = this.find(y);

        if (x === y) return;

        if (this.rank[x] < this.rank[y]) {
            [x, y] = [y, x];
        }

        this.parent[y] = x;

        if (this.rank[x] === this.rank[y]) {
            this.rank[x] += 1;
        }
        this.groupCount -= 1;
    }

    samep(x, y) {
        return this.find(x) === this.find(y);
    }
}
