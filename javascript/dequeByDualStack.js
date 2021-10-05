// 配列を2つ使用しての両端キューの実装。
// どちらかの方向に偏るとそちら側の配列が際限なく伸びるので、
// 長期運用には使用しないほうがいい。
// でも、競技プログラミングならこれでいいでしょ……みたいな。
// 存在しない値を取得しようとすると、エラーではなく
// undefined を返すので注意。

class deque {
    // コンストラクタ。
    // 何も渡さなければ要素数 0 で初期化し、
    // 配列を渡せばそれを用いて初期化する。
    constructor(arr) {
        this.dualArray = [[], []];
        this.offset = 0;
        this.length = 0;
        if (arr instanceof Array && arr.length > 0) {
            for (value of arr) {
                this.push(value);
            }
        }
    }

    // 渡されたインデックスから、内部動作上のインデックスを返す関数。
    // [1, x] なら右側の配列、[0, x] なら左側の配列とする。
    getIndex(pos) {
        if (pos +  this.offset >= 0) {
            return [1, pos + this.offset];
        } else {
            return [0, -(pos + this.offset)-1];
        }
    }

    // value を右端に追加
    push(value) {
        let [lr, idx] = this.getIndex(this.length);
        if (lr === 0) {
            this.dualArray[lr][idx] = value;
            this.length += 1;
        } else {
            this.dualArray[lr].push(value);
            this.length += 1;
        }
    }

    // value を左端に追加
    pushLeft(value) {
        let [lr, idx] = this.getIndex(-1);
        if (lr === 0) {
            this.dualArray[lr].push(value);
            this.offset -= 1;
            this.length += 1;
        } else {
            this.dualArray[lr][idx] = value;
            this.offset -= 1;
            this.length += 1;
        }
    }

    // 右端の要素を削除し、値を返す
    pop() {
        if (this.length === 0) {
            return undefined;
        }
        let [lr, idx] = this.getIndex(this.length-1);
        if (lr === 0) {
            this.length -= 1;
            return this.dualArray[lr][idx];
        } else {
            this.length -= 1;
            return this.dualArray[lr].pop();
        }
    }

    // 左端の要素を削除し、値を返す
    popLeft() {
        if (this.length === 0) {
            return undefined;
        }
        let [lr, idx] = this.getIndex(0);
        if (lr === 0) {
            this.offset += 1;
            this.length -= 1;
            return this.dualArray[lr].pop();
        } else {
            this.offset += 1;
            this.length -= 1;
            return this.dualArray[lr][idx]
        }
    }

    // 指定したインデックスの値を取得する。
    get (pos) {
        if (pos < 0) {
            pos = this.length + pos;
        }
        if (pos < 0 || this.length <= pos) {
            return undefined;
        }
        let[lr, idx] = this.getIndex(pos);
        return this.dualArray[lr][idx];
    }
}
