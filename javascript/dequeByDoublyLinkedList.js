// 双方向連結リストによる、両端キューの実装。
// 学習の一環として作成。
// 実際のところ早くない……が、長期運用にも耐える構造のはず。
// 存在しない値を取得しようとすると、エラーではなく undefined を
// 返すので注意。

// 両端キュー用ノードのクラス
class dequeNode {
    constructor(value) {
        this.left = null;
        this.right = null;
        this.value = value;
    }
}

class deque {
    // コンストラクタ。
    // 何も渡さなければ、要素数 0 にて初期化のみ行い、
    // Array を渡せば、それを用いて初期化する。
    constructor(arr) {
        this.root = new dequeNode(null);
        this.root.left = this.root;
        this.root.right = this.root;
        this.length = 0;
        if (arr instanceof Array && arr.length > 0) {
            for (let value of arr) {
                this.push(value);
            }
        }
    }

    // 参照ノードの左側に値を追加し、追加した要素の参照を返す
    insertLeft(ref, value) {
        if (!ref instanceof dequeNode) {
            return undefined;
        } else {
            const obj = new dequeNode(value);
            ref.left.right = obj;
            obj.left = ref.left;
            ref.left = obj;
            obj.right = ref;
            this.length += 1;
            return obj;
        }
    }

    // 参照ノードの右側に値を追加し、追加した要素の参照を返す
    insertRight(ref, value) {
        if (!ref instanceof dequeNode) {
            return undefined;
        } else {
            const obj = new dequeNode(value);
            ref.right.left = obj;
            obj.right = ref.right;
            ref.right = obj;
            obj.left = ref;
            this.length += 1;
            return obj;
        }
    }

    // 右端に値を追加し、追加した要素の参照を返す
    push(value) {
        return this.insertLeft(this.root, value);
    }

    // 左端に値を追加し、追加した要素の参照を返す
    pushLeft(value) {
        return this.insertRight(this.root, value);
    }

    // 参照ノードを削除し、その値を返す
    pop_ref(ref) {
        if (ref === this.root) {
            return undefined;
        } else {
            ref.right.left = ref.left;
            ref.left.right = ref.right;
            this.length -= 1;
            return ref.value;
        }
    }

    // 右端の要素を削除し、その値を返す
    pop() {
        if (this.length === 0) {
            return undefined;
        } else {
            const ref = this.root.left;
            return this.pop_ref(ref);
        }
    }

    // 左端の要素を削除し、その値を返す
    popLeft() {
        if (this.length === 0) {
            return undefined;
        } else {
            const ref = this.root.right;
            return this.pop_ref(ref);
        }
    }

    // 左から pos-1 番目の値を取得する
    get(pos) {
        if (pos < 0) {
            pos = this.length + pos;
        }
        if (pos >= this.length) {
            return undefined;
        }

        // 一応近い方から数えるように……。
        if (pos < this.length / 2) {
            let nd = this.root.right;
            for (let i = 0; i < pos; i++) {
                nd = nd.right;
            }
            return nd.value;
        } else {
            let nd = this.root.left;
            for (let i = 0; i < this.length - pos - 1; i++) {
                nd = nd.left;
            }
            return nd.value;
        }
    }
}
